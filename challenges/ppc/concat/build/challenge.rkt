#lang racket

(require "parser.rkt")
(require "test-cases.rkt")

(define (run-challenge)
  (for ([test-case test-cases])
    (let* ([description (car test-case)]
           [expected (cdr test-case)])
      (printf "描述: ~a\n" description)
      (printf "🐱> ")
      (let* ([input (read-line)]
             [parsed (parse-concat-lang input)])
        (if (equal? parsed expected)
            (printf "正确!\n\n")
            (begin
              (printf "不正确。正确答案是: ~a\n" (format "~a" expected))
              (printf "你的回答解析为: ~a\n\n" (format "~a" parsed))
              (exit 1)))))))

(run-challenge)
(printf "恭喜! 你已经通过了所有测试。\n")
