package com.google.cloud.solutions.samples.iot.dataflow.io;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import org.joda.time.Instant;

import com.google.api.services.bigquery.model.TableFieldSchema;
import com.google.api.services.bigquery.model.TableRow;
import com.google.api.services.bigquery.model.TableSchema;
import com.google.cloud.dataflow.sdk.transforms.DoFn;
import com.google.cloud.dataflow.sdk.values.KV;
import com.google.cloud.solutions.samples.iot.dataflow.messages.Alert;
import com.google.cloud.solutions.samples.iot.dataflow.messages.Message;

public class BQIOTSchema implements Serializable {

  private static final long serialVersionUID = 1L;

  static String DEVICE_ID = "device_id";
  static String TIMESTAMP = "timestamp";
  static String LIGHTLEVEL = "lightLevel";
  static String BUTTONPRESSED = "button_pressed";
  static String TEMPERATURE = "temp";
  static String HUMIDITY = "humidity";
  static String REGION = "region";
  static String CITY = "city";
  static String OR_X = "orientation_x";
  static String OR_Y = "orientation_y";
  static String OR_Z = "orientation_z";
  static String HOSTNAME = "hostname";
  static String IP_ADDRESS = "ip_address";

  static String KEY = "key";
  static String MSG = "msg";

  public static TableSchema getRawDataSchema() {
    List<TableFieldSchema> fields = new ArrayList<TableFieldSchema>();

    fields.add(new TableFieldSchema().setName(DEVICE_ID).setType("STRING"));
    fields.add(new TableFieldSchema().setName(TIMESTAMP).setType("TIMESTAMP"));
    fields.add(new TableFieldSchema().setName(LIGHTLEVEL).setType("INTEGER"));
    fields.add(new TableFieldSchema().setName(BUTTONPRESSED).setType("BOOLEAN"));
    fields.add(new TableFieldSchema().setName(TEMPERATURE).setType("FLOAT"));
    fields.add(new TableFieldSchema().setName(HUMIDITY).setType("FLOAT"));
    fields.add(new TableFieldSchema().setName(REGION).setType("STRING"));
    fields.add(new TableFieldSchema().setName(CITY).setType("STRING"));
    fields.add(new TableFieldSchema().setName(OR_X).setType("FLOAT"));
    fields.add(new TableFieldSchema().setName(OR_Y).setType("FLOAT"));
    fields.add(new TableFieldSchema().setName(OR_Z).setType("FLOAT"));
    fields.add(new TableFieldSchema().setName(HOSTNAME).setType("STRING"));
    fields.add(new TableFieldSchema().setName(IP_ADDRESS).setType("STRING"));


    TableSchema schema = new TableSchema().setFields(fields);
    return schema;
  }

  @SuppressWarnings("serial")
  public static class CreateRawDataRowFn extends DoFn<Message, TableRow> implements Serializable {

    @Override
    public void processElement(DoFn<Message, TableRow>.ProcessContext c) throws Exception {
      TableRow row = new TableRow();

      row.set(DEVICE_ID, c.element().device_id);
      row.set(TIMESTAMP, c.element().timestamp);
      row.set(LIGHTLEVEL, c.element().light_level);
      row.set(BUTTONPRESSED, c.element().button_pressed);
      row.set(TEMPERATURE, c.element().temperature);
      row.set(HUMIDITY, c.element().humidity);
      row.set(REGION, c.element().region);
      row.set(CITY, c.element().city);
      row.set(OR_X, c.element().orientation_x);
      row.set(OR_Y, c.element().orientation_y);
      row.set(OR_Z, c.element().orientation_z);
      row.set(HOSTNAME, c.element().hostname);
      row.set(IP_ADDRESS, c.element().ip_address);

      c.output(row);

    }

  }

  public static TableSchema getAlertSchema() {
    
    List<TableFieldSchema> fields = new ArrayList<TableFieldSchema>();
    
    fields.add(new TableFieldSchema().setName(KEY).setType("STRING"));
    fields.add(new TableFieldSchema().setName(TIMESTAMP).setType("TIMESTAMP"));
    fields.add(new TableFieldSchema().setName(MSG).setType("STRING"));

    TableSchema schema = new TableSchema().setFields(fields);
    return schema;
  
  }

  @SuppressWarnings("serial")
  public static class CreateAlertRowFn extends DoFn<KV<String,Alert>, TableRow> implements Serializable {

    @Override
    public void processElement(DoFn<KV<String,Alert>, TableRow>.ProcessContext c) throws Exception {
      
      TableRow row = new TableRow();
      
      row.set(KEY, c.element().getValue().key);
      row.set(TIMESTAMP, c.element().getValue().timestamp.getMillis()/1000);
      row.set(MSG, c.element().getValue().msg);

      c.output(row);

    }

  }

}
