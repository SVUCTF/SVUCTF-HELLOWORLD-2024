#lang racket/base

(provide test-cases)

(define test-cases
  (list
   ;; cat
   (list "一只猫"
         '(sequence (position (adjacent (over (multiple (concat (subject "cat")))))))
         "真是会虚情假意呢")

   ;; [cat]
   (list "一只猫在盒子里"
         '(sequence (position (adjacent (over (multiple (concat (container #f
                                                                           (opt-pos (position (adjacent (over (multiple (concat (subject "cat")))))))
                                                                           #f)))))))
         "到现在都还执着于过去")

   ;; cat / [c]at
   (list "一只猫把头放进盒子里，另一只猫叠在这个盒子上"
         '(sequence (position (adjacent (over (multiple (concat (subject "cat")))
                                              #f
                                              (position (adjacent (over (multiple (concat (container #f
                                                                                                     (opt-pos (position (adjacent (over (multiple (concat (subject "c")))))))
                                                                                                     #f)
                                                                                          "at")))))))))
         "真难看，你讲的话和做的事全都互相矛盾")

   ;; [cat + @] / [cat] / [cat]
   (list "猫猫叠叠乐，三层叠放的盒子，每层盒子里都有一只猫，最上层的猫右侧还有个纱线球"
         '(sequence (position (adjacent (over (multiple (concat (container #f
                                                                           (opt-pos (position (adjacent (adjacent (over (multiple (concat (subject "cat")))))
                                                                                                        #f
                                                                                                        (over (multiple (concat (subject "@")))))))
                                                                           #f)))
                                              #f
                                              (position (adjacent (over (multiple (concat (container #f
                                                                                                     (opt-pos (position (adjacent (over (multiple (concat (subject "cat")))))))
                                                                                                     #f)))
                                                                        #f
                                                                        (position (adjacent (over (multiple (concat (container #f
                                                                                                                               (opt-pos (position (adjacent (over (multiple (concat (subject "cat")))))))
                                                                                                                               #f)))))))))))))
         "CRYCHIC 已经毁了，绝对不可能再复活了")

   ;; [cat + @] / [cat] / [cat] => dog + @
   (list "突然一只狗把刚刚猫猫叠叠乐的盒子撞飞了，猫咪也被吓跑了。描述从「猫猫叠叠乐」到「只剩下一只狗 (dog) 和纱线球」的过程"
         '(sequence (position (adjacent (over (multiple (concat (container #f
                                                                           (opt-pos (position (adjacent (adjacent (over (multiple (concat (subject "cat")))))
                                                                                                        #f
                                                                                                        (over (multiple (concat (subject "@")))))))
                                                                           #f)))
                                              #f
                                              (position (adjacent (over (multiple (concat (container #f
                                                                                                     (opt-pos (position (adjacent (over (multiple (concat (subject "cat")))))))
                                                                                                     #f)))
                                                                        #f
                                                                        (position (adjacent (over (multiple (concat (container #f
                                                                                                                               (opt-pos (position (adjacent (over (multiple (concat (subject "cat")))))))
                                                                                                                               #f))))))))))))
                    #f
                    (sequence (position (adjacent (adjacent (over (multiple (concat (subject "dog")))))
                                                  #f
                                                  (over (multiple (concat (subject "@"))))))))
         "🤓☝️诶！但是我可以给你一个 Flag：")
   ))
