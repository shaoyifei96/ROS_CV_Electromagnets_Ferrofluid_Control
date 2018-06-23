;; Auto-generated. Do not edit!


(when (boundp 'image_transport_tutorial::tracking2Dmsg)
  (if (not (find-package "IMAGE_TRANSPORT_TUTORIAL"))
    (make-package "IMAGE_TRANSPORT_TUTORIAL"))
  (shadow 'tracking2Dmsg (find-package "IMAGE_TRANSPORT_TUTORIAL")))
(unless (find-package "IMAGE_TRANSPORT_TUTORIAL::TRACKING2DMSG")
  (make-package "IMAGE_TRANSPORT_TUTORIAL::TRACKING2DMSG"))

(in-package "ROS")
;;//! \htmlinclude tracking2Dmsg.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass image_transport_tutorial::tracking2Dmsg
  :super ros::object
  :slots (_header _x _y _nx _ny ))

(defmethod image_transport_tutorial::tracking2Dmsg
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:x __x) 0)
    ((:y __y) 0)
    ((:nx __nx) 0)
    ((:ny __ny) 0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _x (round __x))
   (setq _y (round __y))
   (setq _nx (round __nx))
   (setq _ny (round __ny))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:nx
   (&optional __nx)
   (if __nx (setq _nx __nx)) _nx)
  (:ny
   (&optional __ny)
   (if __ny (setq _ny __ny)) _ny)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; uint16 _x
    2
    ;; uint16 _y
    2
    ;; uint16 _nx
    2
    ;; uint16 _ny
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; uint16 _x
       (write-word _x s)
     ;; uint16 _y
       (write-word _y s)
     ;; uint16 _nx
       (write-word _nx s)
     ;; uint16 _ny
       (write-word _ny s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; uint16 _x
     (setq _x (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; uint16 _y
     (setq _y (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; uint16 _nx
     (setq _nx (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; uint16 _ny
     (setq _ny (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get image_transport_tutorial::tracking2Dmsg :md5sum-) "e9ae025fecda7be954c017b760906dc6")
(setf (get image_transport_tutorial::tracking2Dmsg :datatype-) "image_transport_tutorial/tracking2Dmsg")
(setf (get image_transport_tutorial::tracking2Dmsg :definition-)
      "Header header
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

")



(provide :image_transport_tutorial/tracking2Dmsg "e9ae025fecda7be954c017b760906dc6")


