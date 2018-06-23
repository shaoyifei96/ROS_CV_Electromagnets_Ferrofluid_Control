// Auto-generated. Do not edit!

// (in-package image_transport_tutorial.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class tracking2Dmsg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.x = null;
      this.y = null;
      this.nx = null;
      this.ny = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('x')) {
        this.x = initObj.x
      }
      else {
        this.x = 0;
      }
      if (initObj.hasOwnProperty('y')) {
        this.y = initObj.y
      }
      else {
        this.y = 0;
      }
      if (initObj.hasOwnProperty('nx')) {
        this.nx = initObj.nx
      }
      else {
        this.nx = 0;
      }
      if (initObj.hasOwnProperty('ny')) {
        this.ny = initObj.ny
      }
      else {
        this.ny = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type tracking2Dmsg
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [x]
    bufferOffset = _serializer.uint16(obj.x, buffer, bufferOffset);
    // Serialize message field [y]
    bufferOffset = _serializer.uint16(obj.y, buffer, bufferOffset);
    // Serialize message field [nx]
    bufferOffset = _serializer.uint16(obj.nx, buffer, bufferOffset);
    // Serialize message field [ny]
    bufferOffset = _serializer.uint16(obj.ny, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type tracking2Dmsg
    let len;
    let data = new tracking2Dmsg(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [x]
    data.x = _deserializer.uint16(buffer, bufferOffset);
    // Deserialize message field [y]
    data.y = _deserializer.uint16(buffer, bufferOffset);
    // Deserialize message field [nx]
    data.nx = _deserializer.uint16(buffer, bufferOffset);
    // Deserialize message field [ny]
    data.ny = _deserializer.uint16(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'image_transport_tutorial/tracking2Dmsg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e9ae025fecda7be954c017b760906dc6';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
    uint16 x
    uint16 y
    uint16 nx
    uint16 ny
    
    
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    # 0: no frame
    # 1: global frame
    string frame_id
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new tracking2Dmsg(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.x !== undefined) {
      resolved.x = msg.x;
    }
    else {
      resolved.x = 0
    }

    if (msg.y !== undefined) {
      resolved.y = msg.y;
    }
    else {
      resolved.y = 0
    }

    if (msg.nx !== undefined) {
      resolved.nx = msg.nx;
    }
    else {
      resolved.nx = 0
    }

    if (msg.ny !== undefined) {
      resolved.ny = msg.ny;
    }
    else {
      resolved.ny = 0
    }

    return resolved;
    }
};

module.exports = tracking2Dmsg;
