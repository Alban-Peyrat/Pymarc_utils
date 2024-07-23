# Test plan

_Expected results are viewed with MarcEdit here, except if I forget to turn empty indicators into backslashes_

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
=001  000002
=200  1\$aLove Colored Master Spark
=330  \\$aRésumé
=610  \\$9123$9456$aJardin chinois$cRenard$bPoisson$8987$8654$zfre
=610  \\$9789$aBois$zeng
=615  \\$0963$fNuclear$aSolar$zgra
=620  \\$aMaiden$zytu$5258$kCapriccio
=701  \1$aRose$bSummer$4070
```

## Record `000003` : test `force_indicators()`

* `200` : neither indicator should change and stay `1` then empty
* `330` : both `330` should change to `3` then empty as indicators
* `701` : first indicator should be `9` and the second one stay `1`
* `702` : first indicator should stay the same as `0` and the second one should be `8`

Result should be :

```
=LDR  00216nam  2200097   45e0
=001  000003
=200  1 $aLove Colored Master Spark
=330  3 $aRésumé
=330  3 $aRésumé n°2
=701  91$aRose$bSummer$4070
=702  08$aBranwen$bRaven$4070
```

## Record `000004` : test `add_missing_subfield_to_field()`

* `701` _Rose_ : last subfield should be a new `$z`
* `701` _Branwen_ : a new `$z` should be in 6th position, between `$4630` & `$4999`
* `701` _Schnee_ : a `$z` is already here, so no new `$z` should appear

Result should be :

```
=LDR  00148nam a2200073   45e0
=001  000004
=200  1\$aLove Colored Master Spark
=330  \\$aRésumé
=701  \1$aRose$bSummer$4070$zfre
=701  \1$aBranwen$bRaven$cQrow$4070$4630$zfre$4999$4888$4777$4666
=701  \1$aSchnee$bWinter$zeng
```

## Record `000005` : test `edit_specific_repeatable_subfield_content_with_regexp()`

* `101` : all `$a` and `$cgat` should only be 3 characters long, `$d` still has spaces, `$cFR` should still have spaces
* `102` : on both `102`, all `$a` and `$cGE` should only be 2 characters long, `$d` still has spaces, `$cfre` should still have spaces
* `200` : on both `200`, all `$e` that were only spaces should be empty, the other should have content, the `$a` with only spaces should still only be spaces
* `330` : the first one (_éditeur_) should have a empty `$a`, the second one (_moi_) should still have spaces

Result should be :

```
=LDR  00406nam  2200133   45e0
=001  000005
=101  11$afre$d  fre   $aeng$ajap$cgat$c  FR
=102  11$aFR$d  FR   $aUK$aSP$cGE$c  fre
=102  11$aFR$cGB$d  IT  
=200  1\$aLove Colored Master Spark$e$eNuclear Fusion$e$a    $eHistory of the moon
=200  1\$aEndless$e$a    $eNow
=330  \\$a$2editeur
=330  \\$a    $2moi
=701  \1$aRose$bSummer$4070
```

## Record `000006` : test `replace_specific_repeatable_subfield_content_not_matching_regexp()`

* `101` : first `$a` & `c` should be `und`, `$d` still has spaces, `$aeng` should still be there
* `102` :
  * On the first one, first `$a` & `c` should be `??`, `$d` still has spaces, `$aUK` should still be there
  * On the second one, `$a` should be `??`, `$d` still has spaces, `$cGB` should still be there
* `200` : on both `200`, all `$e` not starting with `in :` should be `ARA ARA ARA`, the other are unchanged
* `330` : the first one (_éditeur_) should have be `Résumé invalide`, the second one (_moi_) should still have spaces

Result should be :

```
=LDR  00386nam  2200133   45e0
=001  000006
=101  11$aund$d  fre   $aeng$cund
=102  11$a??$d  FR   $aUK$c??
=102  11$a??$cGB$d  IT  
=200  1\$aLove Colored Master Spark$ein : Nuclear Fusion$a    $eARA ARA ARA
=200  1\$aEndless$ein : Now$a    $eARA ARA ARA
=330  \\$aRésumé invalide$2editeur
=330  \\$a    $2moi
=701  \1$aRose$bSummer$4070
```

## Record `000007` : test `merge_all_fields_by_tag()`

* _Big sort tests are done in the record testing sorting functions_
* `099` should have `12` as indicators and have `$tLIV` → `$x` → `$tART`
* `181` should have empty indicators and have `$6` → `$a` → `$2`

Result should be :

```
=LDR  00255nam  2200133   45e0
=001  000007
=099  12$tLIV$x0$tART
=181  \\$6Rose$arenard$2rda
=200  1\$aLove Colored Master Spark
=330  \\$aRésumé
=701  \1$aRose$bSummer$4070
```

## Record `000008` : test `split_tags_if_multiple_specific_subfield()`

* Should have 3 `463` _Nuclear Fusion_ with only 1 `$t`, they should be indentical except for the `$t`
* Should alse have a `463` _History of the moon_ with no common values with the other 3

Result should be :

```
=LDR  00249nam  2200085   45e0
=001  000000
=200  1\$aLove Colored Master Spark
=463  02$aNuclear Fusion$0123456$x12$x34$tBird
=463  02$aNuclear Fusion$0123456$x12$x34$tRenard
=463  02$aNuclear Fusion$0123456$x12$x34$tPoisson
=463  95$aHistory of the moon$tHibou$987654$x98$x76
=701  \1$aRose$bSummer$4070
```

_Note : History of the moon actually end up first as the new fields are appended after it_

## Record `000009` : test `split_merged_tags()`

* First `777` (with _Schnee_) : 3 `$a`, 1 `$f`, 2 `$4` : should end up in 3 `777`, all of them with the same `$f`, _BRANWEN (Raven)_ should have a `$4651` while the others two have `$4651` (because _ROSE (Summer)_ is the correct index & _SCHNEE (Winter)_ is out of range, so it copies the first one)
* Second `777` (without _Schnee_) should be split in two identical field, except for the `$a` the same except for 
* Third `777` (_Xiao Long_) should stay as it is
* `999` : should be splitted in `$aSTET$bADM123456$c750 CAT` & `$aMRSL$bADM987654$c621 POM`, as all subfields appears the same number of times & their order should stay the same

Result should be :

```
=LDR  00364nam  2200109   45e0
=001  000009
=200  1\$aLove Colored Master Spark
=330  \\$aRésumé
=777  \1$aROSE (Summer)$f19..-....$4070
=777  \1$aBRANWEN (Raven)$f19..-....$4651
=777  \1$aSCHNEE (Winter)$f19..-....$4070
=777  \1$aROSE (Ruby)$f1885-1978$4999
=777  \1$aBRANWEN (Qrow)$f1885-1978$4999
=777  \1$aXIAO LONG (Yang)$4000
=995  \1$aSTET$bADM123456$c750 CAT
=995  \1$aMRSL$bADM987654$c621 POM
```