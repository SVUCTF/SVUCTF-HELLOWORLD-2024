#lang racket/base

(require "parser.rkt")
(require "test-cases.rkt")

(file-stream-buffer-mode (current-input-port) 'none)
(file-stream-buffer-mode (current-output-port) 'none)

(define parse-error-responses
  '("语法都不对，做不来的事就别轻易说出口"
    "连语法都会出错，有办法背负其他人的人生吗"
    "没有人拜托你那样写语法，这是最后的警告"))

(define incorrect-responses
  '("连题目的要求听不进去，你这个人真是满脑子都想着自己呢"
    "今后不要再和我扯上关系了"))

(define (random-response responses)
  (list-ref responses (random (length responses))))

(define (run-challenge [test-cases test-cases])
  (if (null? test-cases)
      (let ([flag (getenv "GZCTF_FLAG")])
        (if flag
            (displayln flag)
            (displayln "错误：未找到 Flag 环境变量")))
      (let* ([test-case (car test-cases)]
             [description (car test-case)]
             [expected (cadr test-case)]
             [response (caddr test-case)])
        (printf "祥子：~a\n" description)
        (display "soyo：")
        (with-handlers
            ([exn:fail?
              (lambda (_exn)
                (printf "祥子：~a\n" (random-response parse-error-responses)))])
          (let ([parsed (parse-concat-lang (read-line))])
            (if (equal? parsed expected)
                (begin
                  (printf "祥子：~a\n" response)
                  (displayln "------------------------------")
                  (run-challenge (cdr test-cases)))
                (begin
                  (printf "祥子：~a\n" (random-response incorrect-responses)))))))))

(run-challenge)
