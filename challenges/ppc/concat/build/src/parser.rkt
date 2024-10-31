#lang racket/base

(require "grammar.rkt")
(require "tokenizer.rkt")

(provide parse-concat-lang)

(define (parse-concat-lang input)
  (parse-to-datum (tokenize (open-input-string input))))
