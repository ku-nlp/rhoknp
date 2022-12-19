# Juman++/KNP Format

This page describes the format of the result of Juman++ and KNP.

## Juman++

Juman++ is a morphological analyzer for Japanese.
We show an example of the result of Juman++:

```
# Language analysis of "麻生太郎はコーヒーを買って飲んだ。"
麻生 あそう 麻生 名詞 6 人名 5 * 0 * 0 "人名:日本:姓:135:0.00166"
太郎 たろう 太郎 名詞 6 人名 5 * 0 * 0 "人名:日本:名:45:0.00106"
は は は 助詞 9 副助詞 2 * 0 * 0 NIL
コーヒー こーひー コーヒー 名詞 6 普通名詞 1 * 0 * 0 "代表表記:珈琲/こーひー ドメイン:料理・食事 カテゴリ:人工物-食べ物"
を を を 助詞 9 格助詞 1 * 0 * 0 NIL
買って かって 買う 動詞 2 * 0 子音動詞ワ行 12 タ系連用テ形 14 "代表表記:買う/かう ドメイン:家庭・暮らし;ビジネス 反義:動詞:売る/うる"
飲んだ のんだ 飲む 動詞 2 * 0 子音動詞マ行 9 タ形 10 "代表表記:飲む/のむ ドメイン:料理・食事"
。 。 。 特殊 1 句点 1 * 0 * 0 NIL
EOS
```

Each line represents a morpheme (a.k.a. *keitai-so*) and formatted as `[surface form] [reading] [lemma] [pos] [pos ID] [pos subcategory] [pos subcategory ID] [conjugation type] [conjugation type ID] [conjugation form] [conjugation form ID] [semantic information]`.
For example, `飲んだ のんだ 飲む 動詞 2 * 0 子音動詞マ行 9 タ形 10 "代表表記:飲む/のむ ドメイン:料理・食事"` indicates that the surface form is `飲んだ`, the reading is `のんだ`, the lemma is `飲む`, and the pos (part-of-speech) is `動詞`, and so forth.

## KNP

KNP is a Japanese dependency parser.
We show an example of the result of KNP:

```
# Language analysis of "麻生太郎はコーヒーを買って飲んだ。"
* 3D <文頭><人名><ハ><助詞><体言><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><正規化代表表記:麻生/あそう+太郎/たろう><主辞代表表記:太郎/たろう>
+ 1D <文節内><係:文節内><文頭><人名><体言><名詞項候補><先行詞候補><SM-人><SM-主体><正規化代表表記:麻生/あそう>
麻生 あそう 麻生 名詞 6 人名 5 * 0 * 0 "人名:日本:姓:135:0.00166 疑似代表表記 代表表記:麻生/あそう" <人名:日本:姓:135:0.00166><疑似代表表記><代表表記:麻生/あそう><正規化代表表記:麻生/あそう><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><固有キー><用言表記先頭><用言表記末尾><用言意味表記末尾>
+ 4D <人名><ハ><助詞><体言><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><名詞項候補><先行詞候補><SM-人><SM-主体><正規化代表表記:太郎/たろう><主辞代表表記:太郎/たろう><Wikipedia上位語:政治家><Wikipediaエントリ:麻生太郎><解析格:ガ>
太郎 たろう 太郎 名詞 6 人名 5 * 0 * 0 "人名:日本:名:45:0.00106 疑似代表表記 代表表記:太郎/たろう" <人名:日本:名:45:0.00106><疑似代表表記><代表表記:太郎/たろう><正規化代表表記:太郎/たろう><Wikipedia上位語:政治家:0-1><Wikipediaエントリ:麻生太郎:0-1><漢字><かな漢字><名詞相当語><自立><複合←><内容語><タグ単位始><固有キー><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
は は は 助詞 9 副助詞 2 * 0 * 0 NIL <かな漢字><ひらがな><付属>
* 2D <BGH:珈琲/こーひー><ヲ><助詞><体言><係:ヲ格><区切:0-0><格要素><連用要素><正規化代表表記:珈琲/こーひー><主辞代表表記:珈琲/こーひー>
+ 3D <BGH:珈琲/こーひー><ヲ><助詞><体言><係:ヲ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:珈琲/こーひー><主辞代表表記:珈琲/こーひー><解析格:ヲ>
コーヒー こーひー コーヒー 名詞 6 普通名詞 1 * 0 * 0 "代表表記:珈琲/こーひー ドメイン:料理・食事 カテゴリ:人工物-食べ物" <代表表記:珈琲/こーひー><ドメイン:料理・食事><カテゴリ:人工物-食べ物><正規化代表表記:珈琲/こーひー><記英数カ><カタカナ><名詞相当語><自立><内容語><タグ単位始><文節始><固有キー><文節主辞>
を を を 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
* 3D <BGH:買う/かう><用言:動><係:連用><レベル:A><区切:3-5><ID:〜て（用言）><連用要素><連用節><動態述語><正規化代表表記:買う/かう><主辞代表表記:買う/かう>
+ 4D <BGH:買う/かう><用言:動><係:連用><レベル:A><区切:3-5><ID:〜て（用言）><連用要素><連用節><動態述語><正規化代表表記:買う/かう><主辞代表表記:買う/かう><用言代表表記:買う/かう><節-区切><節-主辞><格関係2:ヲ:コーヒー><格解析結果:買う/かう:動1:ガ/U/-/-/-/-;ヲ/C/コーヒー/2/0/1;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:買う/かう>
買って かって 買う 動詞 2 * 0 子音動詞ワ行 12 タ系連用テ形 14 "代表表記:買う/かう ドメイン:家庭・暮らし;ビジネス 反義:動詞:売る/うる" <代表表記:買う/かう><ドメイン:家庭・暮らし;ビジネス><反義:動詞:売る/うる><正規化代表表記:買う/かう><かな漢字><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
* -1D <BGH:飲む/のむ><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:飲む/のむ><主辞代表表記:飲む/のむ>
+ -1D <BGH:飲む/のむ><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:飲む/のむ><主辞代表表記:飲む/のむ><用言代表表記:飲む/のむ><節-区切><節-主辞><主題格:一人称優位><格関係1:ガ:太郎><格解析結果:飲む/のむ:動8:ガ/N/太郎/1/0/1;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;デ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:飲む/のむ>
飲んだ のんだ 飲む 動詞 2 * 0 子音動詞マ行 9 タ形 10 "代表表記:飲む/のむ ドメイン:料理・食事" <代表表記:飲む/のむ><ドメイン:料理・食事><正規化代表表記:飲む/のむ><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
EOS
```

The line starting with `*` represents the beginning of a phrase (a.k.a. *bunsetsu*) and formatted as `* [parent phrase index][dependency type] [semantic information]`.
For example, the line `* 3D <文頭><人名>` indicates that the phrase modifies the `3`rd phrase with the dependency type of `D` includes the semantic information of `<文頭>` and `<人名>`.

The line starting with `+` represents the beginning of a base-phrase (a.k.a. *kihon-ku*) and formatted as `+ [parent base-phrase index][dependency type] [semantic information]`.
For example, the line `+ 1D <文節内><係:文節内>` indicates that the base-phrase modifies the `1`st base-phrase with the dependency type of `D` includes the semantic information of `<文節内>` and `<係:文節内>`.

Lines with neither `*` nor `+` represent morphemes.
The format is almost the same as Juman++'s one, except that the column of representing the semantic information is added at the end.

## Misc

- Lines starting with `#` are comments.
- `EOS` represents the end of the sentence.

---

## Reference

- [KNPの基本的な出力の読み方 (in Japanese)](http://cr.fvcrc.i.nagoya-u.ac.jp/~sasano/knp/format.html)
