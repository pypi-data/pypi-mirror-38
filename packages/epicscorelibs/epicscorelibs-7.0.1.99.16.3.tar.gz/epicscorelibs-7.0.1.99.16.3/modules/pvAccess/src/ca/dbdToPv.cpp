/**
 * Copyright - See the COPYRIGHT that is included with this distribution.
 * pvAccessCPP is distributed subject to a Software License Agreement found
 * in file LICENSE that is included with this distribution.
 */


#include <epicsVersion.h>
#include <sstream>
#include <alarm.h>
#include <alarmString.h>

#include <pv/standardField.h>
#include <pv/logger.h>
#include <pv/pvAccess.h>
#include <pv/reftrack.h>
#include <pv/convert.h>
#include <pv/timeStamp.h>
#include "caChannel.h"
#define epicsExportSharedSymbols
#include "dbdToPv.h"

using namespace epics::pvData;
using std::string;
using std::ostringstream;

namespace epics {
namespace pvAccess {
namespace ca {

#define CA_PRIORITY 50

static void enumChoicesHandler(struct event_handler_args args)
{
    DbdToPv *dbdToPv = static_cast<DbdToPv*>(args.usr);
    dbdToPv->getChoicesDone(args);
}

static void description_connection_handler(struct connection_handler_args args)
{
    DbdToPv *dbdToPv = static_cast<DbdToPv*>(ca_puser(args.chid));
    dbdToPv->descriptionConnected(args);
}

static void descriptionHandler(struct event_handler_args args)
{
    DbdToPv *dbdToPv = static_cast<DbdToPv*>(args.usr);
    dbdToPv->getDescriptionDone(args);
}

DbdToPvPtr DbdToPv::create(
    CAChannelPtr const & caChannel,
    PVStructurePtr const & pvRequest,
    IOType ioType)
{
    DbdToPvPtr dbdToPv(new DbdToPv(ioType));
    dbdToPv->activate(caChannel,pvRequest);
    return dbdToPv;
}

DbdToPv::DbdToPv(IOType ioType)
:  ioType(ioType),
   fieldRequested(false),
   alarmRequested(false),
   timeStampRequested(false),
   displayRequested(false),
   controlRequested(false),
   valueAlarmRequested(false),
   isArray(false),
   firstTime(true),
   choicesValid(false),
   waitForChoicesValid(false),
   caValueType(-1),
   caRequestType(-1),
   maxElements(0)
{
   caTimeStamp.secPastEpoch = 0;
   caTimeStamp.nsec = 0;
}

static ScalarType dbr2ST[] =
{
    pvString,   // DBR_STRING = 0
    pvShort,    // DBR_SHORT. DBR_INT = 1
    pvFloat,    // DBR_FLOAT = 2
    static_cast<ScalarType>(-1),         // DBR_ENUM = 3
    pvByte,     // DBR_CHAR = 4
    pvInt,      // DBR_LONG = 5
    pvDouble    // DBR_DOUBLE = 6
};

static chtype getDbrType(const ScalarType scalarType)
{
    switch(scalarType)
    {
         case pvString : return DBR_STRING;
         case pvByte : return DBR_CHAR;
         case pvShort : return DBR_SHORT;
         case pvInt : return DBR_LONG;
         case pvFloat : return DBR_FLOAT;
         case pvDouble : return DBR_DOUBLE;
         default: break;
    }
    throw  std::runtime_error("getDbr: illegal scalarType");
}


void DbdToPv::activate(
    CAChannelPtr const & caChannel,
    PVStructurePtr const & pvRequest)
{
    chid channelID = caChannel->getChannelID();
    chtype channelType = ca_field_type(channelID);
    caValueType = (channelType==DBR_ENUM ? DBR_ENUM : getDbrType(dbr2ST[channelType]));
    if(!pvRequest) {
        string mess(caChannel->getChannelName());
            mess += " DbdToPv::activate pvRequest is null";
            throw  std::runtime_error(mess);
    } 
    PVStructurePtr fieldPVStructure;
    if(pvRequest->getPVFields().size()==0) {
         fieldPVStructure = pvRequest;
    } else {
         fieldPVStructure = pvRequest->getSubField<PVStructure>("field");
    }
    if(!fieldPVStructure) {
        ostringstream mess;
        mess << caChannel->getChannelName()
          << " DbdToPv::activate illegal pvRequest " << pvRequest;
        throw std::runtime_error(mess.str());
    } 
    if(fieldPVStructure->getPVFields().size()==0) 
    {
        fieldRequested = true;
        alarmRequested = true;
        timeStampRequested = true;
        displayRequested = true;
        controlRequested = true;
        valueAlarmRequested = true;
    } else {
        if(fieldPVStructure->getSubField("value")) fieldRequested = true;
        if(fieldPVStructure->getSubField("alarm")) alarmRequested = true;
        if(fieldPVStructure->getSubField("timeStamp")) timeStampRequested = true;
        if(fieldPVStructure->getSubField("display")) displayRequested = true;
        if(fieldPVStructure->getSubField("control")) controlRequested = true;
        if(fieldPVStructure->getSubField("valueAlarm")) valueAlarmRequested = true;
    }
    switch(ioType)
    {
         case getIO : break;
         case putIO:
              alarmRequested = false;
              timeStampRequested = false;
              displayRequested = false;
              controlRequested = false;
              valueAlarmRequested = false;
              break;
         case monitorIO: break;
    }
    StandardFieldPtr standardField = getStandardField();
    if(channelType==DBR_ENUM)
    {
        displayRequested = false;
        controlRequested = false;
        valueAlarmRequested = false;
        string properties;
        if(alarmRequested && timeStampRequested) {
            properties += "alarm,timeStamp";
        } else if(timeStampRequested) {
            properties += "timeStamp";
        } else if(alarmRequested) {
            properties += "alarm";
        }
        caRequestType = (properties.size()==0 ? DBR_ENUM : DBR_TIME_ENUM);
        structure = standardField->enumerated(properties);
        int result = ca_array_get_callback(DBR_GR_ENUM,
               1,
               channelID, enumChoicesHandler, this);
        if (result == ECA_NORMAL) result = ca_flush_io();
        if (result != ECA_NORMAL) {
            string mess(caChannel->getChannelName());
            mess += " DbdToPv::activate getting enum cnoices ";
            mess += ca_message(result);
            throw  std::runtime_error(mess);
        }
        // NOTE: we do not wait here, since all subsequent request (over TCP) is serialized
        // and will guarantee that enumChoicesHandler is called first
        return;
    }
    maxElements = ca_element_count(channelID);
    if(maxElements!=1) isArray = true;
    if(isArray)
    {
         controlRequested = false;
         valueAlarmRequested = false;
    }
    ScalarType st = dbr2ST[channelType];
    if(st==pvString) {
        displayRequested = false;
        controlRequested = false;
        valueAlarmRequested = false;
    }
    if(controlRequested || displayRequested || valueAlarmRequested) timeStampRequested = false;
    FieldCreatePtr fieldCreate(FieldCreate::getFieldCreate());
    PVDataCreatePtr pvDataCreate(PVDataCreate::getPVDataCreate());
    FieldBuilderPtr fieldBuilder(fieldCreate->createFieldBuilder());
    if(fieldRequested) {
        if(isArray) {
           fieldBuilder->addArray("value",st);
        } else {
           fieldBuilder->add("value",st);
        }
    }
    if(alarmRequested) fieldBuilder->add("alarm",standardField->alarm());
    if(timeStampRequested) fieldBuilder->add("timeStamp",standardField->timeStamp());
    if(displayRequested) fieldBuilder->add("display",standardField->display());
    if(controlRequested) fieldBuilder->add("control",standardField->control());
    if(valueAlarmRequested) {
        switch(st)
        {
           case pvByte:
               fieldBuilder->add("valueAlarm",standardField->byteAlarm()); break;
           case pvShort:
               fieldBuilder->add("valueAlarm",standardField->shortAlarm()); break;
           case pvInt:
               fieldBuilder->add("valueAlarm",standardField->intAlarm()); break;
           case pvFloat:
               fieldBuilder->add("valueAlarm",standardField->floatAlarm()); break;
           case pvDouble:
               fieldBuilder->add("valueAlarm",standardField->doubleAlarm()); break;
           default:
               throw  std::runtime_error("DbDToPv::activate: bad type");
        }
    }
    structure = fieldBuilder->createStructure();
    caRequestType = caValueType;
    if(displayRequested || controlRequested || valueAlarmRequested)
    {
       caRequestType = dbf_type_to_DBR_CTRL(caValueType); 
    } else if(timeStampRequested || alarmRequested) {
       caRequestType = dbf_type_to_DBR_TIME(caValueType);
    } else {
       caRequestType = dbf_type_to_DBR(caValueType);
    }
    if(displayRequested) {
         chid channelID;
         string name(caChannel->getChannelName() + ".DESC");
         int result = ca_create_channel(name.c_str(),
             description_connection_handler,
             this,
             CA_PRIORITY, // TODO mapping
             &channelID);
         if (result == ECA_NORMAL) result = ca_flush_io();
         if (result != ECA_NORMAL) {
            string mess(caChannel->getChannelName());
            mess += " DbdToPv::activate getting description ";
            mess += ca_message(result);
            throw  std::runtime_error(mess);
        }
    }
}

void DbdToPv::descriptionConnected(struct connection_handler_args args)
{
    if (args.op != CA_OP_CONN_UP) return;
    ca_array_get_callback(DBR_STRING,
         0,
         args.chid, descriptionHandler, this);
}

void DbdToPv::getDescriptionDone(struct event_handler_args &args)
{
    if(args.status!=ECA_NORMAL) return;
    const dbr_string_t *value = static_cast<const dbr_string_t *>(dbr_value_ptr(args.dbr,DBR_STRING));
    description = string(*value);
    ca_clear_channel(args.chid);
}

void DbdToPv::getChoicesDone(struct event_handler_args &args)
{
    if(args.status!=ECA_NORMAL)
    {
        string message("DbdToPv::getChoicesDone ca_message ");
        message += ca_message(args.status);
        throw std::runtime_error(message);
    }
    const dbr_gr_enum* dbr_enum_p = static_cast<const dbr_gr_enum*>(args.dbr);
    size_t num = dbr_enum_p->no_str;
    choices.reserve(num);
    for(size_t i=0; i<num; ++i) choices.push_back(string(&dbr_enum_p->strs[i][0]));
    bool signal = false;
    {
        Lock lock(choicesMutex);  
        choicesValid = true;
        if(waitForChoicesValid) signal = true;
    }
    if(signal) choicesEvent.signal();
} 

chtype DbdToPv::getRequestType()
{
    if(caRequestType<0) {
       throw  std::runtime_error("DbDToPv::getRequestType: bad type");
    }
    return caRequestType;
}

PVStructurePtr DbdToPv::createPVStructure()
{
    return getPVDataCreate()->createPVStructure(structure);
}

template<typename dbrT, typename pvT>
void copy_DBRScalar(const void * dbr, PVScalar::shared_pointer const & pvScalar)
{
    std::tr1::shared_ptr<pvT> value = std::tr1::static_pointer_cast<pvT>(pvScalar);
    value->put(static_cast<const dbrT*>(dbr)[0]);
}

template<typename dbrT, typename pvT>
void copy_DBRScalarArray(const void * dbr, unsigned count, PVScalarArray::shared_pointer const & pvArray)
{
    std::tr1::shared_ptr<pvT> value = std::tr1::static_pointer_cast<pvT>(pvArray);
    typename pvT::svector temp(value->reuse());
    temp.resize(count);
    std::copy(
        static_cast<const dbrT*>(dbr),
        static_cast<const dbrT*>(dbr) + count,
        temp.begin());
    value->replace(freeze(temp));
}

template<typename dbrT>
void get_DBRControl(const void * dbr, double *upper_ctrl_limit,double *lower_ctrl_limit)
{
    *upper_ctrl_limit =  static_cast<const dbrT*>(dbr)->upper_ctrl_limit;
    *lower_ctrl_limit =  static_cast<const dbrT*>(dbr)->lower_ctrl_limit;
}

template<typename dbrT>
void get_DBRDisplay(
    const void * dbr, double *upper_disp_limit,double *lower_disp_limit,string *units)
{
    *upper_disp_limit =  static_cast<const dbrT*>(dbr)->upper_disp_limit;
    *lower_disp_limit =  static_cast<const dbrT*>(dbr)->lower_disp_limit;
     *units = static_cast<const dbrT*>(dbr)->units;
}

template<typename dbrT>
void get_DBRValueAlarm(
    const void * dbr,
    double *upper_alarm_limit,double *upper_warning_limit,
    double *lower_warning_limit,double *lower_alarm_limit)
{
    *upper_alarm_limit =  static_cast<const dbrT*>(dbr)->upper_alarm_limit;
    *upper_warning_limit =  static_cast<const dbrT*>(dbr)->upper_warning_limit;
    *lower_warning_limit =  static_cast<const dbrT*>(dbr)->lower_warning_limit;
    *lower_alarm_limit =  static_cast<const dbrT*>(dbr)->lower_alarm_limit;
}

Status DbdToPv::getFromDBD(
     PVStructurePtr const & pvStructure,
     BitSet::shared_pointer const & bitSet,
     struct event_handler_args &args)
{
   if(args.status!=ECA_NORMAL)
   {
     Status errorStatus(Status::STATUSTYPE_ERROR, string(ca_message(args.status)));
     return errorStatus;
   }
   if(fieldRequested)
   {
       void * value = dbr_value_ptr(args.dbr,caRequestType);
       if(isArray) {
           long count = args.count;
           PVScalarArrayPtr pvValue = pvStructure->getSubField<PVScalarArray>("value");
           switch(caValueType) {
           case DBR_STRING:
           {
                const dbr_string_t *dbrval = static_cast<const dbr_string_t *>(value);
                PVStringArrayPtr pvValue = pvStructure->getSubField<PVStringArray>("value");
                PVStringArray::svector arr(pvValue->reuse());
                arr.resize(count);
                std::copy(dbrval, dbrval + count, arr.begin());
                pvValue->replace(freeze(arr));
                break;
           }
           case DBR_CHAR:
               copy_DBRScalarArray<dbr_char_t,PVByteArray>(value,count,pvValue);
               break;
           case DBR_SHORT:
               copy_DBRScalarArray<dbr_short_t,PVShortArray>(value,count,pvValue);
               break;
           case DBR_LONG:
               copy_DBRScalarArray<dbr_long_t,PVIntArray>(value,count,pvValue);
               break;
           case DBR_FLOAT:
               copy_DBRScalarArray<dbr_float_t,PVFloatArray>(value,count,pvValue);
               break;
           case DBR_DOUBLE:
               copy_DBRScalarArray<dbr_double_t,PVDoubleArray>(value,count,pvValue);
               break;
           default:
                Status errorStatus(
                    Status::STATUSTYPE_ERROR, string("DbdToPv::getFromDBD logic error"));
                return errorStatus;
           }
       } else {
           PVScalarPtr pvValue = pvStructure->getSubField<PVScalar>("value");
           switch(caValueType) {
           case DBR_ENUM:
           {
                const dbr_enum_t *dbrval = static_cast<const dbr_enum_t *>(value);
                PVIntPtr value = pvStructure->getSubField<PVInt>("value.index");
                value->put(*dbrval);
                PVStringArrayPtr pvChoices
                     = pvStructure->getSubField<PVStringArray>("value.choices");
                if(pvChoices->getLength()==0)
                {
                     ConvertPtr convert = getConvert();
                     size_t n = choices.size();
                     pvChoices->setLength(n);
                     convert->fromStringArray(pvChoices,0,n,choices,0);       
                     bitSet->set(pvStructure->getSubField("value")->getFieldOffset());
                } else {
                     bitSet->set(value->getFieldOffset());
                }
                break;
           }
           case DBR_STRING: copy_DBRScalar<dbr_string_t,PVString>(value,pvValue); break;
           case DBR_CHAR: copy_DBRScalar<dbr_char_t,PVByte>(value,pvValue); break;
           case DBR_SHORT: copy_DBRScalar<dbr_short_t,PVShort>(value,pvValue); break;
           case DBR_LONG: copy_DBRScalar<dbr_long_t,PVInt>(value,pvValue); break;
           case DBR_FLOAT: copy_DBRScalar<dbr_float_t,PVFloat>(value,pvValue); break;
           case DBR_DOUBLE: copy_DBRScalar<dbr_double_t,PVDouble>(value,pvValue); break;
           default:
                Status errorStatus(
                    Status::STATUSTYPE_ERROR, string("DbdToPv::getFromDBD logic error"));
                return errorStatus;
           }
       }
       if(caValueType!=DBR_ENUM) {
            bitSet->set(pvStructure->getSubField("value")->getFieldOffset());
       }
    }
    if(alarmRequested) {
        // Note that status and severity are aways the first two members of DBR_ 
        const dbr_sts_string *data = static_cast<const dbr_sts_string *>(args.dbr);
        dbr_short_t status = data->status;
        dbr_short_t severity = data->severity;
        bool statusChanged = false;
        bool severityChanged = false;
        PVStructurePtr pvAlarm(pvStructure->getSubField<PVStructure>("alarm"));
        PVIntPtr pvSeverity(pvAlarm->getSubField<PVInt>("severity"));
        if(caAlarm.severity!=severity) {
            caAlarm.severity = severity;
            pvSeverity->put(severity);
            severityChanged = true;
        }
        PVStringPtr pvMessage(pvAlarm->getSubField<PVString>("message"));
        PVIntPtr pvStatus(pvAlarm->getSubField<PVInt>("status"));
        if(caAlarm.status!=status) {
            caAlarm.status = status;
            pvStatus->put(status);
            string message("UNKNOWN STATUS");
            if(status<=ALARM_NSTATUS) message = string(epicsAlarmConditionStrings[status]);
            pvMessage->put(message);
            statusChanged = true;
        }
        if(statusChanged&&severityChanged) {
            bitSet->set(pvAlarm->getFieldOffset());
        } else if(severityChanged) {
            bitSet->set(pvSeverity->getFieldOffset());
        } else if(statusChanged) {
            bitSet->set(pvStatus->getFieldOffset());
            bitSet->set(pvMessage->getFieldOffset());
        }
    }
    if(timeStampRequested) {
        // Note that epicsTimeStamp always follows status and severity
        const dbr_time_string *data = static_cast<const dbr_time_string *>(args.dbr);
        epicsTimeStamp stamp = data->stamp;
        PVStructurePtr pvTimeStamp(pvStructure->getSubField<PVStructure>("timeStamp"));
        if(caTimeStamp.secPastEpoch!=stamp.secPastEpoch) {
            caTimeStamp.secPastEpoch = stamp.secPastEpoch;
            PVLongPtr pvSeconds(pvTimeStamp->getSubField<PVLong>("secondsPastEpoch"));
            pvSeconds->put(stamp.secPastEpoch+posixEpochAtEpicsEpoch);
            bitSet->set(pvSeconds->getFieldOffset());
        }
        if(caTimeStamp.nsec!=stamp.nsec) {
            caTimeStamp.secPastEpoch = stamp.secPastEpoch;
            PVIntPtr pvNano(pvTimeStamp->getSubField<PVInt>("nanoseconds"));
            pvNano->put(stamp.nsec);
            bitSet->set(pvNano->getFieldOffset());
        }
    }
    if(controlRequested)
    {
         double upper_ctrl_limit = 0.0;
         double lower_ctrl_limit = 0.0;
         switch(caRequestType) {
             case DBR_CTRL_CHAR:
                 get_DBRControl<dbr_ctrl_char>(args.dbr,&upper_ctrl_limit,&lower_ctrl_limit); break;
             case DBR_CTRL_SHORT:
                 get_DBRControl<dbr_ctrl_short>(args.dbr,&upper_ctrl_limit,&lower_ctrl_limit); break;
             case DBR_CTRL_LONG:
                 get_DBRControl<dbr_ctrl_long>(args.dbr,&upper_ctrl_limit,&lower_ctrl_limit); break;
             case DBR_CTRL_FLOAT:
                 get_DBRControl<dbr_ctrl_float>(args.dbr,&upper_ctrl_limit,&lower_ctrl_limit); break;
             case DBR_CTRL_DOUBLE:
                 get_DBRControl<dbr_ctrl_double>(args.dbr,&upper_ctrl_limit,&lower_ctrl_limit); break;
             default :
                 throw  std::runtime_error("DbdToPv::getFromDBD logic error");
         }
         PVStructurePtr pvControl(pvStructure->getSubField<PVStructure>("control"));
         if(caControl.upper_ctrl_limit!=upper_ctrl_limit) {
             caControl.upper_ctrl_limit = upper_ctrl_limit;
             PVDoublePtr pv = pvControl->getSubField<PVDouble>("limitHigh");
             pv->put(upper_ctrl_limit);
             bitSet->set(pv->getFieldOffset());
         }
         if(caControl.lower_ctrl_limit!=lower_ctrl_limit) {
             caControl.lower_ctrl_limit = lower_ctrl_limit;
             PVDoublePtr pv = pvControl->getSubField<PVDouble>("limitLow");
             pv->put(lower_ctrl_limit);
             bitSet->set(pv->getFieldOffset());
         }
    }
    if(displayRequested)
    {
        string units;
        string format;
        double upper_disp_limit = 0.0;
        double lower_disp_limit = 0.0;
        switch(caRequestType) {
             case DBR_CTRL_CHAR:
                 get_DBRDisplay<dbr_ctrl_char>(args.dbr,&upper_disp_limit,&lower_disp_limit,&units);
                 format = "I4"; break;
             case DBR_CTRL_SHORT:
                 get_DBRDisplay<dbr_ctrl_short>(args.dbr,&upper_disp_limit,&lower_disp_limit,&units);
                 format = "I6"; break;
             case DBR_CTRL_LONG:
                 get_DBRDisplay<dbr_ctrl_long>(args.dbr,&upper_disp_limit,&lower_disp_limit,&units);
                 format = "I12"; break;
             case DBR_CTRL_FLOAT:
                 get_DBRDisplay<dbr_ctrl_float>(args.dbr,&upper_disp_limit,&lower_disp_limit,&units);
                 {
                 const dbr_ctrl_float *data = static_cast<const dbr_ctrl_float *>(args.dbr);
                 int prec = data->precision;
                 ostringstream s;
                 s << "F" << prec + 6 << "." << prec;
                 format = s.str();
                 }
                 break;
             case DBR_CTRL_DOUBLE:
                 get_DBRDisplay<dbr_ctrl_double>(args.dbr,&upper_disp_limit,&lower_disp_limit,&units);
                 {
                 const dbr_ctrl_double *data = static_cast<const dbr_ctrl_double *>(args.dbr);
                 int prec = data->precision;
                 ostringstream s;
                 s << "F" << prec + 6 << "." << prec;
                 format = s.str();
                 }
                 break;
             default :
                 throw  std::runtime_error("DbdToPv::getFromDBD logic error");
         }
         PVStructurePtr pvDisplay(pvStructure->getSubField<PVStructure>("display"));
         if(caDisplay.lower_disp_limit!=lower_disp_limit) {
            caDisplay.lower_disp_limit = lower_disp_limit;
            PVDoublePtr pvDouble = pvDisplay->getSubField<PVDouble>("limitLow");
            pvDouble->put(lower_disp_limit);
            bitSet->set(pvDouble->getFieldOffset());
         }
         if(caDisplay.upper_disp_limit!=upper_disp_limit) {
            caDisplay.upper_disp_limit = upper_disp_limit;
            PVDoublePtr pvDouble = pvDisplay->getSubField<PVDouble>("limitHigh");
            pvDouble->put(upper_disp_limit);
            bitSet->set(pvDouble->getFieldOffset());
         }
         if(caDisplay.units!=units) {
            caDisplay.units = units;
            PVStringPtr pvString = pvDisplay->getSubField<PVString>("units");
            pvString->put(units);
            bitSet->set(pvString->getFieldOffset());
         }
         if(caDisplay.format!=format) {
            caDisplay.format = format;
            PVStringPtr pvString = pvDisplay->getSubField<PVString>("format");
            pvString->put(format);
            bitSet->set(pvString->getFieldOffset());
         }
         if(!description.empty())
         {
             PVStringPtr pvString = pvDisplay->getSubField<PVString>("description");
             if(description.compare(pvString->get()) !=0) {
                  pvString->put(description);
                  bitSet->set(pvString->getFieldOffset());
             }
         }
    }
    if(valueAlarmRequested) {
        double upper_alarm_limit = 0.0;
        double upper_warning_limit = 0.0;
        double lower_warning_limit = 0.0;
        double lower_alarm_limit = 0.0;
        switch(caRequestType) {
             case DBR_CTRL_CHAR:
                 get_DBRValueAlarm<dbr_ctrl_char>(args.dbr,
                     &upper_alarm_limit,&upper_warning_limit,
                     &lower_warning_limit,&lower_alarm_limit);
                 break;
             case DBR_CTRL_SHORT:
                 get_DBRValueAlarm<dbr_ctrl_short>(args.dbr,
                     &upper_alarm_limit,&upper_warning_limit,
                     &lower_warning_limit,&lower_alarm_limit);
                 break;
             case DBR_CTRL_LONG:
                 get_DBRValueAlarm<dbr_ctrl_long>(args.dbr,
                     &upper_alarm_limit,&upper_warning_limit,
                     &lower_warning_limit,&lower_alarm_limit);
                 break;
             case DBR_CTRL_FLOAT:
                 get_DBRValueAlarm<dbr_ctrl_float>(args.dbr,
                     &upper_alarm_limit,&upper_warning_limit,
                     &lower_warning_limit,&lower_alarm_limit);
                 break;
             case DBR_CTRL_DOUBLE:
                 get_DBRValueAlarm<dbr_ctrl_double>(args.dbr,
                     &upper_alarm_limit,&upper_warning_limit,
                     &lower_warning_limit,&lower_alarm_limit);
                 break;
             default :
                 throw  std::runtime_error("DbdToPv::getFromDBD logic error");
        }
        ConvertPtr convert(getConvert());
        PVStructurePtr pvValueAlarm(pvStructure->getSubField<PVStructure>("valueAlarm"));
        if(caValueAlarm.upper_alarm_limit!=upper_alarm_limit) {
            caValueAlarm.upper_alarm_limit = upper_alarm_limit;
            PVScalarPtr pv = pvValueAlarm->getSubField<PVScalar>("highAlarmLimit");
            convert->fromDouble(pv,upper_alarm_limit);
            bitSet->set(pv->getFieldOffset());
        }
        if(caValueAlarm.upper_warning_limit!=upper_warning_limit) {
            caValueAlarm.upper_warning_limit = upper_warning_limit;
            PVScalarPtr pv = pvValueAlarm->getSubField<PVScalar>("highWarningLimit");
                convert->fromDouble(pv,upper_warning_limit);
            bitSet->set(pv->getFieldOffset());
        }
        if(caValueAlarm.lower_warning_limit!=lower_warning_limit) {
            caValueAlarm.lower_warning_limit = lower_warning_limit;
            PVScalarPtr pv = pvValueAlarm->getSubField<PVScalar>("lowWarningLimit");
            convert->fromDouble(pv,lower_warning_limit);
            bitSet->set(pv->getFieldOffset());
        }
        if(caValueAlarm.lower_alarm_limit!=lower_alarm_limit) {
            caValueAlarm.lower_alarm_limit = lower_alarm_limit;
            PVScalarPtr pv = pvValueAlarm->getSubField<PVScalar>("lowAlarmLimit");
            convert->fromDouble(pv,lower_alarm_limit);
            bitSet->set(pv->getFieldOffset());
        }
    }
    if(firstTime) {
        firstTime = false;
        bitSet->clear();
        bitSet->set(0);
    }
    return Status::Ok;
}

template<typename dbrT, typename pvT>
const void * put_DBRScalar(dbrT *val,PVScalar::shared_pointer const & pvScalar)
{
    std::tr1::shared_ptr<pvT> value = std::tr1::static_pointer_cast<pvT>(pvScalar);
    *val = value->get();
    return val;
}

template<typename dbrT, typename pvT>
const void * put_DBRScalarArray(unsigned long*count, PVScalarArray::shared_pointer const & pvArray)
{
    std::tr1::shared_ptr<pvT> value = std::tr1::static_pointer_cast<pvT>(pvArray);
    *count = value->getLength();
    return value->view().data();
}


Status DbdToPv::putToDBD(
     CAChannelPtr const & caChannel,
     PVStructurePtr const & pvStructure,
     bool block,
     caCallbackFunc putHandler,
     void * userarg)
{
    chid channelID = caChannel->getChannelID();
    const void *pValue = NULL;
    unsigned long count = 1;
    char *ca_stringBuffer(0);
    dbr_char_t   bvalue(0);
    dbr_short_t  svalue(0);
    dbr_long_t   lvalue(0);
    dbr_float_t  fvalue(0);
    dbr_double_t dvalue(0);
    if(isArray) {
       PVScalarArrayPtr pvValue = pvStructure->getSubField<PVScalarArray>("value");
       switch(caValueType) {
           case DBR_STRING:
           {
               PVStringArrayPtr pvValue = pvStructure->getSubField<PVStringArray>("value");
               count = pvValue->getLength();
               if(count<1) break;
               if(count>maxElements) count = maxElements;
               int nbytes = count*MAX_STRING_SIZE;
               ca_stringBuffer = new char[nbytes];
               memset(ca_stringBuffer, 0, nbytes);
               pValue = ca_stringBuffer;
               PVStringArray::const_svector stringArray(pvValue->view());
               char  *pnext = ca_stringBuffer;
               for(size_t i=0; i<count; ++i) {
                   string value = stringArray[i];
                   size_t len = value.length();
                   if (len >= MAX_STRING_SIZE) len = MAX_STRING_SIZE - 1;
                   memcpy(pnext, value.c_str(), len);
                   pnext += MAX_STRING_SIZE;
               }
               break;
           }
           case DBR_CHAR:
               pValue = put_DBRScalarArray<dbr_char_t,PVByteArray>(&count,pvValue);
               break;
           case DBR_SHORT:
               pValue = put_DBRScalarArray<dbr_short_t,PVShortArray>(&count,pvValue);
               break;
           case DBR_LONG:
               pValue = put_DBRScalarArray<dbr_long_t,PVIntArray>(&count,pvValue);
               break;
           case DBR_FLOAT:
               pValue = put_DBRScalarArray<dbr_float_t,PVFloatArray>(&count,pvValue);
               break;
           case DBR_DOUBLE:
               pValue = put_DBRScalarArray<dbr_double_t,PVDoubleArray>(&count,pvValue);
               break;
           default:
                Status errorStatus(
                    Status::STATUSTYPE_ERROR, string("DbdToPv::getFromDBD logic error"));
                return errorStatus;
           }
    } else {
        PVScalarPtr pvValue = pvStructure->getSubField<PVScalar>("value");
        switch(caValueType) {
           case DBR_ENUM:
           {
               bool wait = false;
               {
                   Lock lock(choicesMutex);
                   if(!choicesValid) {
                       wait = true;
                       waitForChoicesValid = true;
                   }
               } 
               bool result = true;
               if(wait) {
                   result = choicesEvent.wait(5.0);
               }
               if(!result) {
                   Status errorStatus(
                    Status::STATUSTYPE_ERROR, string("DbdToPv::getFromDBD "));
                return errorStatus;
               }
               dbr_enum_t indexvalue = pvStructure->getSubField<PVInt>("value.index")->get();
               pValue = &indexvalue;
               break;
           }
           case DBR_STRING: pValue = pvStructure->getSubField<PVString>("value")->get().c_str(); break;
           case DBR_CHAR: pValue = put_DBRScalar<dbr_char_t,PVByte>(&bvalue,pvValue); break;
           case DBR_SHORT: pValue = put_DBRScalar<dbr_short_t,PVShort>(&svalue,pvValue); break;
           case DBR_LONG: pValue = put_DBRScalar<dbr_long_t,PVInt>(&lvalue,pvValue); break;
           case DBR_FLOAT: pValue = put_DBRScalar<dbr_float_t,PVFloat>(&fvalue,pvValue); break;
           case DBR_DOUBLE: pValue = put_DBRScalar<dbr_double_t,PVDouble>(&dvalue,pvValue); break;
           default:
                Status errorStatus(
                    Status::STATUSTYPE_ERROR, string("DbdToPv::getFromDBD logic error"));
                return errorStatus;
         }
    }
    Status status = Status::Ok;
    int result = 0;
    caChannel->attachContext();
    if(block) {
        result = ca_array_put_callback(caValueType,count,channelID,pValue,putHandler,userarg);
    } else {
        result = ca_array_put(caValueType,count,channelID,pValue);
    }
    if(result==ECA_NORMAL) {
         ca_flush_io();
    } else {
         status = Status(Status::STATUSTYPE_ERROR, string(ca_message(result)));
    }
    if(ca_stringBuffer!=NULL) delete[] ca_stringBuffer;
    return status;
}    

}}}
