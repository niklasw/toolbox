
(require :sb-bsd-sockets)
(use-package :sb-bsd-sockets)
(cl:in-package "CL-USER")
;; (cl:defpackage "ARRAY-C-CALL" (:use "CL" "SB-ALIEN" "SB-C-CALL"))
;; (cl:in-package "ARRAY-C-CALL")

(sb-alien:load-shared-object "./libfunctions.so" :dont-save nil)

(sb-alien:define-alien-routine circle_area float (radius float))

(sb-alien:define-alien-routine circle_circumference float (radius float))

;; Test the functions
(let ((area (circle_area 5.0))
      (circ (circle_circumference 5.0)))
  (format t "Result: area ~a and circumference ~a~%" area circ))
