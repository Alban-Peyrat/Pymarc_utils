# Test plan

_Expected results are viewed with MarcEdit here_

## Record `000000` : nothing

Result should be :

```
=LDR  00147nam  2200073   45e0
=001  000000
=200  1\$aLove Colored Master Spark
=330  \\$aRésumé
=701  \1$aRose$aSummer$4070
```

## Record `000001` : test `sort_fields_by_tag()`

`330` is before `200`.

Result should be :

```
=LDR  00147nam  2200073   45e0
=001  000001
=330  \\$aRésumé
=200  1\$aLove Colored Master Spark
=701  \1$aRose$aSummer$4070
```

## Record `000002` : test `sort_subfields_for_tag()`

* `610` (`["9", "a", "*", "8", "z"]`) :
  * Tests if multiple occurrence of this field are all correctly sorted and don't influence each other
  * Tests if using both beginning and ending sorting at the time works
  * Tests if subfield who should not move don't move
  * Tests if multiple occurrence of a sorted subfield keep the same order
  * _Jardin chinois_ :
    * `$9` is supposed to be the first subfield, there are 2 of them
    * `$a` is supposed to be the second subfield
    * `$c` is supposed to be ignored, so it should be between `$a` & `$b`
    * `$b` is supposed to be ignored, so it should be between `$c` & `$8`
    * `$8` is supposed to be the second subfield from the end, there are 2 of them
    * `$z` is supposed to be the last subfield
  * _Bois_ :
    * `$9` is supposed to be the first subfield
    * `$a` is supposed to be the second subfield
    * `$z` is supposed to be the last subfield
* `615` (`["0", "f"]`) :
  * Tests if sorting only at the beginning works
  * `$0` is supposed to be the first subfield
  * `$f` is supposed to be the second subfield
  * `$a` is supposed to be ignored, so it should be between `$f` & `$z`
  * `$z` is supposed to be ignored, so it should be at the end after `$a`
* `620` (`["*", "5", "k"]`) :
  * Tests if sorting only at the end works
  * `$a` is supposed to be ignored, so it should be first before `$z`
  * `$z` is supposed to be ignored, so it should be between `$a` & `$5`
  * `$5` is supposed to be the second subfield from the end
  * `$k` is supposed to be the last subfield

Result should be :

```
=LDR  00337nam  2200121   45e0
=001  000001
=200  1\$aLove Colored Master Spark
=330  \\$aRésumé
=610  \\$9123$9456$aJardin chinois$cRenard$bPoisson$8987$8654$zfre
=610  \\$9789$aBois$zeng
=615  \\$0963$fNuclear$aSolar$zgra
=620  \\$aMaiden$zytu$5258$kCapriccio
=701  \1$aRose$bSummer$4070
```