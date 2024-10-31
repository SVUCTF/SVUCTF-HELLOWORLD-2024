#lang brag

sequence : position
         | position "=>" sequence

position : adjacent

adjacent : over
         | adjacent "+" over

over : multiple
     | multiple "/" position

multiple : concat
         | NUMBER ["*"] multiple
         | NUMBER "/" multiple

concat : subject [NUMBER]
       | [PARTIAL] container [PARTIAL]

container : LSQUARE opt-pos RSQUARE
          | LPAREN opt-pos RPAREN
          | LCURLY opt-pos RCURLY
          | LANGLE opt-pos RANGLE

opt-pos : [position]

subject : CAT
        | PARTIAL
        | ALPHA+
        | "@"
