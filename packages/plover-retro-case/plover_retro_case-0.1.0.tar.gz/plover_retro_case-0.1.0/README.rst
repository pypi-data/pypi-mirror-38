################
Plover Retro Case
################

Retroactively change the case of an already written word

Usage
=====

Retro Case
-----------------------

``{:retro_case:capPrev:capThis:deliminater?}``

-  **letter**: the letter or word to fingerspell
-  **capPrev**: whether to capitalise the previous word
-  **capThis**: whether to capitalise the current word
-  **delimiter** *(optional)*: the character or word to join stitched letters with, *defaults to ''*

Examples
^^^^^^^^

- camelCase

  - camel case{:retro_case:false:true} → camelCase

- PascalCase

  - pascal case{:retro_case:true:true} → PascalCase

- snake_case

  - snake case{:retro_case:false:false:_} → snake_case

