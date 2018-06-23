
(cl:in-package :asdf)

(defsystem "image_transport_tutorial-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :sensor_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "ResizedImage" :depends-on ("_package_ResizedImage"))
    (:file "_package_ResizedImage" :depends-on ("_package"))
    (:file "tracking2Dmsg" :depends-on ("_package_tracking2Dmsg"))
    (:file "_package_tracking2Dmsg" :depends-on ("_package"))
  ))