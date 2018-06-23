; Auto-generated. Do not edit!


(cl:in-package image_transport_tutorial-msg)


;//! \htmlinclude tracking2Dmsg.msg.html

(cl:defclass <tracking2Dmsg> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (x
    :reader x
    :initarg :x
    :type cl:fixnum
    :initform 0)
   (y
    :reader y
    :initarg :y
    :type cl:fixnum
    :initform 0)
   (nx
    :reader nx
    :initarg :nx
    :type cl:fixnum
    :initform 0)
   (ny
    :reader ny
    :initarg :ny
    :type cl:fixnum
    :initform 0))
)

(cl:defclass tracking2Dmsg (<tracking2Dmsg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <tracking2Dmsg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'tracking2Dmsg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name image_transport_tutorial-msg:<tracking2Dmsg> is deprecated: use image_transport_tutorial-msg:tracking2Dmsg instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <tracking2Dmsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader image_transport_tutorial-msg:header-val is deprecated.  Use image_transport_tutorial-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <tracking2Dmsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader image_transport_tutorial-msg:x-val is deprecated.  Use image_transport_tutorial-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <tracking2Dmsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader image_transport_tutorial-msg:y-val is deprecated.  Use image_transport_tutorial-msg:y instead.")
  (y m))

(cl:ensure-generic-function 'nx-val :lambda-list '(m))
(cl:defmethod nx-val ((m <tracking2Dmsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader image_transport_tutorial-msg:nx-val is deprecated.  Use image_transport_tutorial-msg:nx instead.")
  (nx m))

(cl:ensure-generic-function 'ny-val :lambda-list '(m))
(cl:defmethod ny-val ((m <tracking2Dmsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader image_transport_tutorial-msg:ny-val is deprecated.  Use image_transport_tutorial-msg:ny instead.")
  (ny m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <tracking2Dmsg>) ostream)
  "Serializes a message object of type '<tracking2Dmsg>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'x)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'x)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'y)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'y)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'nx)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'nx)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'ny)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'ny)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <tracking2Dmsg>) istream)
  "Deserializes a message object of type '<tracking2Dmsg>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'x)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'x)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'y)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'y)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'nx)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'nx)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'ny)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'ny)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<tracking2Dmsg>)))
  "Returns string type for a message object of type '<tracking2Dmsg>"
  "image_transport_tutorial/tracking2Dmsg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'tracking2Dmsg)))
  "Returns string type for a message object of type 'tracking2Dmsg"
  "image_transport_tutorial/tracking2Dmsg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<tracking2Dmsg>)))
  "Returns md5sum for a message object of type '<tracking2Dmsg>"
  "e9ae025fecda7be954c017b760906dc6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'tracking2Dmsg)))
  "Returns md5sum for a message object of type 'tracking2Dmsg"
  "e9ae025fecda7be954c017b760906dc6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<tracking2Dmsg>)))
  "Returns full string definition for message of type '<tracking2Dmsg>"
  (cl:format cl:nil "Header header~%uint16 x~%uint16 y~%uint16 nx~%uint16 ny~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'tracking2Dmsg)))
  "Returns full string definition for message of type 'tracking2Dmsg"
  (cl:format cl:nil "Header header~%uint16 x~%uint16 y~%uint16 nx~%uint16 ny~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <tracking2Dmsg>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     2
     2
     2
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <tracking2Dmsg>))
  "Converts a ROS message object to a list"
  (cl:list 'tracking2Dmsg
    (cl:cons ':header (header msg))
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':nx (nx msg))
    (cl:cons ':ny (ny msg))
))
