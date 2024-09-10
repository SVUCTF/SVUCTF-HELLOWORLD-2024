#lang racket

(require brag/support)

(provide tokenize)

(define-lex-abbrev digits (:+ (char-set "0123456789")))
(define-lex-abbrev letters (:+ (char-set "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")))

(define (tokenize ip)
  (port-count-lines! ip)
  (define concat-lexer
    (lexer-src-pos
     [digits (token 'NUMBER lexeme)]
     ["cat" (token 'CAT lexeme)]
     [(:or "c" "a" "t" "ca" "at") (token 'PARTIAL lexeme)]
     [letters (token 'ALPHA lexeme)]
     ["=>" (token '=>)]
     ["+" (token '+)]
     ["/" (token '/)]
     ["*" (token '*)]
     ["[" (token 'LSQUARE)]
     ["]" (token 'RSQUARE)]
     ["(" (token 'LPAREN)]
     [")" (token 'RPAREN)]
     ["{" (token 'LCURLY)]
     ["}" (token 'RCURLY)]
     ["<" (token 'LANGLE)]
     [">" (token 'RANGLE)]
     ["@" (token '@ lexeme)]
     [whitespace (token lexeme #:skip? #t)]))
  (define (next-token) (concat-lexer ip))
  next-token)
