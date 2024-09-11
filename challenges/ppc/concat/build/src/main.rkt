#lang racket/base

(require "parser.rkt")
(require "test-cases.rkt")

(define (run-challenge [test-cases test-cases])
  (if (null? test-cases)
      (begin
        (displayln "恭喜，你已经通过了所有测试。")
        (display "Flag：")
        (let ([flag (getenv "GZCTF_FLAG")])
          (if flag
              (displayln flag)
              (displayln "错误：未找到 Flag 环境变量"))))
      (let* ([test-case (car test-cases)]
             [description (car test-case)]
             [expected (cdr test-case)])
        (printf "描述：~a\n" description)
        (display "🐱> ")
        (with-handlers
            ([exn:fail?
              (lambda (_exn)
                (displayln "解析错误"))])
          (let ([parsed (parse-concat-lang (read-line))])
            (if (equal? parsed expected)
                (begin
                  (displayln "正确")
                  (displayln "--------------------")
                  (run-challenge (cdr test-cases)))
                (begin
                  (displayln "不正确哦"))))))))

(run-challenge)
