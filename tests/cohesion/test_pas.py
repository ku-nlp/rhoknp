import logging
import textwrap
from pathlib import Path

from rhoknp.cohesion import ArgumentType, EndophoraArgument, ExophoraArgument, ExophoraReferent
from rhoknp.units import Document


def test_pas_case_analysis() -> None:
    #  echo '彼はご飯を食べ大学へ行った。' | jumanpp | knp -tab
    knp_text = textwrap.dedent(
        """\
        # S-ID:1 KNP:5.0-825c01b7 DATE:2021/10/03 SCORE:-25.47925
        * 4D <SM-主体><SM-人><BGH:彼/かれ><文頭><ハ><助詞><体言><一文字漢字><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><正規化代表表記:彼/かれ><主辞代表表記:彼/かれ>
        + 4D <SM-主体><SM-人><BGH:彼/かれ><文頭><ハ><助詞><体言><一文字漢字><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><名詞項候補><先行詞候補><人称代名詞><正規化代表表記:彼/かれ><主辞代表表記:彼/かれ><解析格:ガ>
        彼 かれ 彼 名詞 6 普通名詞 1 * 0 * 0 "代表表記:彼/かれ カテゴリ:人 漢字読み:訓" <代表表記:彼/かれ><カテゴリ:人><漢字読み:訓><正規化代表表記:彼/かれ><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
        は は は 助詞 9 副助詞 2 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 2D <BGH:御飯/ごはん><ヲ><助詞><体言><係:ヲ格><区切:0-0><格要素><連用要素><正規化代表表記:御飯/ごはん><主辞代表表記:御飯/ごはん>
        + 2D <BGH:御飯/ごはん><ヲ><助詞><体言><係:ヲ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:御飯/ごはん><主辞代表表記:御飯/ごはん><解析格:ヲ>
        ご飯 ごはん ご飯 名詞 6 普通名詞 1 * 0 * 0 "代表表記:御飯/ごはん ドメイン:料理・食事 カテゴリ:人工物-食べ物" <代表表記:御飯/ごはん><ドメイン:料理・食事><カテゴリ:人工物-食べ物><正規化代表表記:御飯/ごはん><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始><文節主辞>
        を を を 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 4P <BGH:食べる/たべる><用言:動><係:連用><レベル:B><並キ:述:&レベル:強><区切:3-5><ID:動詞連用><連用要素><連用節><動態述語><正規化代表表記:食べる/たべる><主辞代表表記:食べる/たべる><並列類似度:1.587><並結句数:2><並結文節数:2><提題受:30>
        + 4P <BGH:食べる/たべる><用言:動><係:連用><レベル:B><並キ:述:&レベル:強><区切:3-5><ID:動詞連用><連用要素><連用節><動態述語><正規化代表表記:食べる/たべる><主辞代表表記:食べる/たべる><用言代表表記:食べる/たべる><提題受:30><節-区切><節-主辞><格関係1:ヲ:ご飯><格解析結果:食べる/たべる:動1:ガ/U/-/-/-/-;ヲ/C/ご飯/1/0/1;ニ/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:食べる/たべる>
        食べ たべ 食べる 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:食べる/たべる ドメイン:料理・食事" <代表表記:食べる/たべる><ドメイン:料理・食事><正規化代表表記:食べる/たべる><かな漢字><活用語><連用形名詞化疑><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        * 4D <SM-主体><SM-場所><SM-組織><BGH:大学/だいがく><ヘ><助詞><体言><係:ヘ格><区切:0-0><格要素><連用要素><正規化代表表記:大学/だいがく><主辞代表表記:大学/だいがく>
        + 4D <SM-主体><SM-場所><SM-組織><BGH:大学/だいがく><ヘ><助詞><体言><係:ヘ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:大学/だいがく><主辞代表表記:大学/だいがく><解析格:ヘ>
        大学 だいがく 大学 名詞 6 普通名詞 1 * 0 * 0 "代表表記:大学/だいがく ドメイン:教育・学習 カテゴリ:場所-施設 組織名末尾" <代表表記:大学/だいがく><ドメイン:教育・学習><カテゴリ:場所-施設><組織名末尾><正規化代表表記:大学/だいがく><漢字><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始><文節主辞>
        へ へ へ 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:行く/いく><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:行く/いく><主辞代表表記:行く/いく>
        + -1D <BGH:行く/いく><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:行く/いく><主辞代表表記:行く/いく><用言代表表記:行く/いく><節-区切><節-主辞><主題格:一人称優位><格関係0:ガ:彼><格関係3:ヘ:大学><格解析結果:行く/いく:動12:ガ/N/彼/0/0/1;ニ/U/-/-/-/-;デ/U/-/-/-/-;ヘ/C/大学/3/0/1;時間/U/-/-/-/-><標準用言代表表記:行く/いく>
        行った いった 行く 動詞 2 * 0 子音動詞カ行促音便形 3 タ形 10 "代表表記:行く/いく ドメイン:交通 反義:動詞:帰る/かえる 付属動詞候補（タ系）" <代表表記:行く/いく><ドメイン:交通><反義:動詞:帰る/かえる><付属動詞候補（タ系）><正規化代表表記:行く/いく><移動動詞><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
        EOS
        """
    )
    doc = Document.from_knp(knp_text)
    # <格解析結果:行く/いく:動12:ガ/N/彼/0/0/1;ニ/U/-/-/-/-;デ/U/-/-/-/-;ヘ/C/大学/3/0/1;時間/U/-/-/-/->
    pas = doc.base_phrases[4].pas
    assert pas is not None
    assert pas.predicate.cfid == "行く/いく:動12"
    assert pas.sid == "1"
    assert pas.cases == ["ガ", "ヘ"]

    # 彼 ガ 行った
    argument_base_phrase = doc.base_phrases[0]  # 彼は
    argument = pas.get_arguments("ガ", relax=False)[0]
    assert isinstance(argument, EndophoraArgument)
    assert argument.type == ArgumentType("N")
    assert argument.base_phrase == argument_base_phrase
    assert argument.phrase == argument_base_phrase.phrase
    assert argument.clause == argument_base_phrase.clause
    assert argument.sentence == argument_base_phrase.sentence
    assert argument.document == argument_base_phrase.document

    # 大学 ヘ 行った
    argument_base_phrase = doc.base_phrases[3]  # 大学へ
    argument = pas.get_arguments("ヘ", relax=False)[0]
    assert isinstance(argument, EndophoraArgument)
    assert argument.type == ArgumentType("C")
    assert argument.base_phrase == argument_base_phrase
    assert argument.phrase == argument_base_phrase.phrase
    assert argument.clause == argument_base_phrase.clause
    assert argument.sentence == argument_base_phrase.sentence
    assert argument.document == argument_base_phrase.document


def test_pas_pas() -> None:
    #  echo '彼はご飯を食べ大学へ行った。' | jumanpp | knp -tab -anaphora
    knp_text = textwrap.dedent(
        """\
        # S-ID:1 KNP:5.0-825c01b7 DATE:2021/10/03 SCORE:-25.47925
        * 4D <SM-主体><SM-人><BGH:彼/かれ><文頭><ハ><助詞><体言><一文字漢字><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><正規化代表表記:彼/かれ><主辞代表表記:彼/かれ>
        + 4D <SM-主体><SM-人><BGH:彼/かれ><文頭><ハ><助詞><体言><一文字漢字><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><名詞項候補><先行詞候補><人称代名詞><正規化代表表記:彼/かれ><主辞代表表記:彼/かれ><照応詞候補:彼><解析格:ガ><EID:5>
        彼 かれ 彼 名詞 6 普通名詞 1 * 0 * 0 "代表表記:彼/かれ カテゴリ:人 漢字読み:訓" <代表表記:彼/かれ><カテゴリ:人><漢字読み:訓><正規化代表表記:彼/かれ><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
        は は は 助詞 9 副助詞 2 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 2D <BGH:御飯/ごはん><ヲ><助詞><体言><係:ヲ格><区切:0-0><格要素><連用要素><正規化代表表記:御飯/ごはん><主辞代表表記:御飯/ごはん>
        + 2D <BGH:御飯/ごはん><ヲ><助詞><体言><係:ヲ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:御飯/ごはん><主辞代表表記:御飯/ごはん><照応詞候補:ご飯><解析格:ヲ><EID:6>
        ご飯 ごはん ご飯 名詞 6 普通名詞 1 * 0 * 0 "代表表記:御飯/ごはん ドメイン:料理・食事 カテゴリ:人工物-食べ物" <代表表記:御飯/ごはん><ドメイン:料理・食事><カテゴリ:人工物-食べ物><正規化代表表記:御飯/ごはん><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始><文節主辞>
        を を を 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 4P <BGH:食べる/たべる><用言:動><係:連用><レベル:B><並キ:述:&レベル:強><区切:3-5><ID:動詞連用><連用要素><連用節><動態述語><正規化代表表記:食べる/たべる><主辞代表表記:食べる/たべる><並列類似度:1.587><並結句数:2><並結文節数:2><提題受:30>
        + 4P <BGH:食べる/たべる><用言:動><係:連用><レベル:B><並キ:述:&レベル:強><区切:3-5><ID:動詞連用><連用要素><連用節><動態述語><正規化代表表記:食べる/たべる><主辞代表表記:食べる/たべる><用言代表表記:食べる/たべる><提題受:30><節-区切><節-主辞><格関係1:ヲ:ご飯><標準用言代表表記:食べる/たべる><EID:7><述語項構造:食べる/たべる:動1:ガ/N/彼/0/0/5;ヲ/C/ご飯/0/1/6;ニ/E/著者/2/-1/0;ト/-/-/-/-/-;デ/-/-/-/-/-;カラ/-/-/-/-/-;ヨリ/-/-/-/-/-;マデ/-/-/-/-/-;ヘ/-/-/-/-/-;時間/-/-/-/-/-;外の関係/-/-/-/-/-;修飾/-/-/-/-/-><省略解析信頼度:0.253><ガ格省略解析信頼度:0.000>
        食べ たべ 食べる 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:食べる/たべる ドメイン:料理・食事" <代表表記:食べる/たべる><ドメイン:料理・食事><正規化代表表記:食べる/たべる><かな漢字><活用語><連用形名詞化疑><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        * 4D <SM-主体><SM-場所><SM-組織><BGH:大学/だいがく><ヘ><助詞><体言><係:ヘ格><区切:0-0><格要素><連用要素><正規化代表表記:大学/だいがく><主辞代表表記:大学/だいがく>
        + 4D <SM-主体><SM-場所><SM-組織><BGH:大学/だいがく><ヘ><助詞><体言><係:ヘ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:大学/だいがく><主辞代表表記:大学/だいがく><照応詞候補:大学><解析格:ヘ><EID:8>
        大学 だいがく 大学 名詞 6 普通名詞 1 * 0 * 0 "代表表記:大学/だいがく ドメイン:教育・学習 カテゴリ:場所-施設 組織名末尾" <代表表記:大学/だいがく><ドメイン:教育・学習><カテゴリ:場所-施設><組織名末尾><正規化代表表記:大学/だいがく><漢字><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始><文節主辞>
        へ へ へ 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:行く/いく><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:行く/いく><主辞代表表記:行く/いく>
        + -1D <BGH:行く/いく><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:行く/いく><主辞代表表記:行く/いく><用言代表表記:行く/いく><節-区切><節-主辞><主題格:一人称優位><格関係0:ガ:彼><格関係3:ヘ:大学><標準用言代表表記:行く/いく><EID:9><述語項構造:行く/いく:動12:ガ/N/彼/0/0/5;ニ/E/著者/2/-1/0;ト/-/-/-/-/-;デ/-/-/-/-/-;カラ/-/-/-/-/-;ヨリ/-/-/-/-/-;マデ/-/-/-/-/-;ヘ/C/大学/0/3/8;時間/-/-/-/-/-;外の関係/-/-/-/-/-;修飾/-/-/-/-/-;ノ/-/-/-/-/-><省略解析信頼度:0.777><ガ格省略解析信頼度:0.000>
        行った いった 行く 動詞 2 * 0 子音動詞カ行促音便形 3 タ形 10 "代表表記:行く/いく ドメイン:交通 反義:動詞:帰る/かえる 付属動詞候補（タ系）" <代表表記:行く/いく><ドメイン:交通><反義:動詞:帰る/かえる><付属動詞候補（タ系）><正規化代表表記:行く/いく><移動動詞><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
        EOS
        """
    )
    doc = Document.from_knp(knp_text)
    # <EID:9><述語項構造:行く/いく:動12:ガ/N/彼/0/0/5;ニ/E/著者/2/-1/0;ト/-/-/-/-/-;デ/-/-/-/-/-;カラ/-/-/-/-/-;ヨリ/-/-/-/-/-;マデ/-/-/-/-/-;ヘ/C/大学/0/3/8;時間/-/-/-/-/-;外の関係/-/-/-/-/-;修飾/-/-/-/-/-;ノ/-/-/-/-/->
    pas = doc.base_phrases[4].pas
    assert pas is not None
    assert pas.predicate.cfid == "行く/いく:動12"
    assert pas.sid == "1"
    assert pas.cases == ["ガ", "ニ", "ヘ"]

    # 彼 ガ 行った
    argument_phrase = doc.base_phrases[0]  # 彼は
    argument = pas.get_arguments("ガ", relax=False)[0]
    assert isinstance(argument, EndophoraArgument)
    assert argument.type == ArgumentType("N")
    assert argument.base_phrase == argument_phrase
    assert argument.phrase == argument_phrase.phrase
    assert argument.clause == argument_phrase.clause
    assert argument.sentence == argument_phrase.sentence
    assert argument.document == argument_phrase.document

    # 著者 ニ 行く
    argument = pas.get_arguments("ニ", relax=False)[0]
    assert isinstance(argument, ExophoraArgument)
    assert argument.type == ArgumentType("E")
    assert argument.exophora_referent == ExophoraReferent("著者")
    assert argument.eid == 0


def test_pas_inter_sentential() -> None:
    #  echo '彼はご飯を食べ大学へ行った。' | jumanpp | knp -tab -anaphora
    knp_text = textwrap.dedent(
        """\
        # S-ID:000-0
        * 2D <SM-主体><SM-人><BGH:彼/かれ><文頭><ハ><助詞><体言><一文字漢字><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><正規化代表表記:彼/かれ><主辞代表表記:彼/かれ>
        + 2D <SM-主体><SM-人><BGH:彼/かれ><文頭><ハ><助詞><体言><一文字漢字><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><名詞項候補><先行詞候補><人称代名詞><正規化代表表記:彼/かれ><主辞代表表記:彼/かれ><照応詞候補:彼><解析格:ガ><EID:5>
        彼 かれ 彼 名詞 6 普通名詞 1 * 0 * 0 "代表表記:彼/かれ カテゴリ:人 漢字読み:訓" <代表表記:彼/かれ><カテゴリ:人><漢字読み:訓><正規化代表表記:彼/かれ><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
        は は は 助詞 9 副助詞 2 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 2D <BGH:御飯/ごはん><ヲ><助詞><体言><係:ヲ格><区切:0-0><格要素><連用要素><正規化代表表記:御飯/ごはん><主辞代表表記:御飯/ごはん>
        + 2D <BGH:御飯/ごはん><ヲ><助詞><体言><係:ヲ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:御飯/ごはん><主辞代表表記:御飯/ごはん><照応詞候補:ご飯><解析格:ヲ><EID:6>
        ご飯 ごはん ご飯 名詞 6 普通名詞 1 * 0 * 0 "代表表記:御飯/ごはん ドメイン:料理・食事 カテゴリ:人工物-食べ物" <代表表記:御飯/ごはん><ドメイン:料理・食事><カテゴリ:人工物-食べ物><正規化代表表記:御飯/ごはん><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始><文節主辞>
        を を を 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:食べる/たべる><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:食べる/たべる><主辞代表表記:食べる/たべる>
        + -1D <BGH:食べる/たべる><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:食べる/たべる><主辞代表表記:食べる/たべる><用言代表表記:食べる/たべる><節-区切><節-主辞><主題格:一人称優位><格関係0:ガ:彼><格関係1:ヲ:ご飯><標準用言代表表記:食べる/たべる><EID:7><述語項構造:食べる/たべる:動1:ガ/N/彼/0/0/5;ヲ/C/ご飯/0/1/6;ニ/E/著者/2/-1/0;ト/-/-/-/-/-;デ/-/-/-/-/-;カラ/-/-/-/-/-;ヨリ/-/-/-/-/-;マデ/-/-/-/-/-;ヘ/-/-/-/-/-;時間/-/-/-/-/-;外の関係/-/-/-/-/-;修飾/-/-/-/-/-><省略解析信頼度:0.173><ガ格省略解析信頼度:0.000>
        食べた たべた 食べる 動詞 2 * 0 母音動詞 1 タ形 10 "代表表記:食べる/たべる ドメイン:料理・食事" <代表表記:食べる/たべる><ドメイン:料理・食事><正規化代表表記:食べる/たべる><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
        EOS
        # S-ID:000-1
        * 1D <SM-主体><SM-場所><SM-組織><BGH:大学/だいがく><文頭><ヘ><助詞><体言><係:ヘ格><区切:0-0><格要素><連用要素><正規化代表表記:大学/だいがく><主辞代表表記:大学/だいがく>
        + 1D <SM-主体><SM-場所><SM-組織><BGH:大学/だいがく><文頭><ヘ><助詞><体言><係:ヘ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:大学/だいがく><主辞代表表記:大学/だいがく><照応詞候補:大学><解析格:ヘ><EID:5>
        大学 だいがく 大学 名詞 6 普通名詞 1 * 0 * 0 "代表表記:大学/だいがく ドメイン:教育・学習 カテゴリ:場所-施設 組織名末尾" <代表表記:大学/だいがく><ドメイン:教育・学習><カテゴリ:場所-施設><組織名末尾><正規化代表表記:大学/だいがく><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
        へ へ へ 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:行く/いく><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:行く/いく><主辞代表表記:行く/いく>
        + -1D <BGH:行く/いく><文末><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:行く/いく><主辞代表表記:行く/いく><用言代表表記:行く/いく><節-区切><節-主辞><主題格:一人称優位><格関係0:ヘ:大学><標準用言代表表記:行く/いく><EID:6><述語項構造:行く/いく:動12:ガ/O/彼/1/0/5;ニ/E/著者/2/-1/2;ト/-/-/-/-/-;デ/-/-/-/-/-;カラ/-/-/-/-/-;ヨリ/-/-/-/-/-;マデ/-/-/-/-/-;ヘ/C/大学/0/0/5;時間/-/-/-/-/-;外の関係/-/-/-/-/-;修飾/-/-/-/-/-;ノ/-/-/-/-/-><省略解析信頼度:0.010><ガ格省略解析信頼度:0.000>
        行った いった 行く 動詞 2 * 0 子音動詞カ行促音便形 3 タ形 10 "代表表記:行く/いく ドメイン:交通 反義:動詞:帰る/かえる 付属動詞候補（タ系）" <代表表記:行く/いく><ドメイン:交通><反義:動詞:帰る/かえる><付属動詞候補（タ系）><正規化代表表記:行く/いく><移動動詞><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
        EOS
        """
    )
    doc = Document.from_knp(knp_text)
    pas = doc.base_phrases[4].pas
    assert pas is not None
    assert pas.predicate.cfid == "行く/いく:動12"
    assert pas.sid == "000-1"
    assert pas.cases == ["ガ", "ニ", "ヘ"]

    # 彼 ガ 行った
    argument_phrase = doc.base_phrases[0]  # 彼は
    argument = pas.get_arguments("ガ", relax=False)[0]
    assert isinstance(argument, EndophoraArgument)
    assert argument.type == ArgumentType("O")
    assert argument.base_phrase == argument_phrase
    assert argument.phrase == argument_phrase.phrase
    assert argument.clause == argument_phrase.clause
    assert argument.sentence == argument_phrase.sentence
    assert argument.document == argument_phrase.document

    # 著者 ニ 行く
    argument = pas.get_arguments("ニ", relax=False)[0]
    assert isinstance(argument, ExophoraArgument)
    assert argument.type == ArgumentType("E")
    assert argument.exophora_referent == ExophoraReferent("著者")
    assert argument.eid == 2


# echo 'こんにちは:' | jumanpp | knp -tab
def test_pas_pas2() -> None:
    knp_text = textwrap.dedent(
        """\
        # S-ID:1 KNP:5.0-825c01b7 DATE:2021/10/04 SCORE:-41.95960
        * 1D <BGH:こんにちは/こんにちは><文頭><感動詞><修飾><係:連用><区切:0-4><連用要素><連用節><正規化代表表記:こんにちは/こんにちは><主辞代表表記:こんにちは/こんにちは>
        + 1D <BGH:こんにちは/こんにちは><文頭><感動詞><修飾><係:連用><区切:0-4><連用要素><連用節><正規化代表表記:こんにちは/こんにちは><主辞代表表記:こんにちは/こんにちは>
        こんにちは こんにちは こんにちは 感動詞 12 * 0 * 0 * 0 "代表表記:こんにちは/こんにちは" <代表表記:こんにちは/こんにちは><正規化代表表記:こんにちは/こんにちは><かな漢字><ひらがな><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
        * -1D <文末><体言><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><裸名詞><提題受:30><主節><状態述語><正規化代表表記::/:><主辞代表表記::/:>
        + -1D <文末><体言><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><裸名詞><提題受:30><主節><状態述語><判定詞句><名詞項候補><先行詞候補><正規化代表表記::/:><主辞代表表記::/:><用言代表表記::/:><CF_NOT_FOUND><節-区切><節-主辞><時制:非過去><格解析結果::/::判0><標準用言代表表記::/:>
        : : : 名詞 6 普通名詞 1 * 0 * 0 "未知語:未対応文字種 品詞推定:特殊 疑似代表表記 代表表記::/: 品詞変更::-:-:-15-1-0-0" <未知語><品詞推定:特殊><疑似代表表記><代表表記::/:><正規化代表表記::/:><品詞変更::-:-:-15-1-0-0-"未知語:未対応文字種 品詞推定:特殊 疑似代表表記 代表表記::/:"><品曖-その他><記英数カ><英記号><記号><名詞相当語><文末><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        EOS
        """
    )
    doc = Document.from_knp(knp_text)
    # <格解析結果::/::判0>
    pas = doc.base_phrases[1].pas
    assert pas is not None
    assert pas.predicate.cfid == ":/::判0"
    assert pas.cases == []


def test_pas_case_analysis2() -> None:
    knp_text = textwrap.dedent(
        """\
        # S-ID:1 KNP:5.0-825c01b7 DATE:2021/10/04 SCORE:-38.18429
        * 1D <BGH:表示/ひょうじ+する/する><文頭><サ変><サ変動詞><連体修飾><用言:動><係:連格><レベル:B><区切:0-5><ID:（動詞連体）><連体節><動態述語><正規化代表表記:表示/ひょうじ><主辞代表表記:表示/ひょうじ>
        + 1D <BGH:表示/ひょうじ+する/する><文頭><サ変動詞><連体修飾><用言:動><係:連格><レベル:B><区切:0-5><ID:（動詞連体）><連体節><動態述語><サ変><正規化代表表記:表示/ひょうじ><主辞代表表記:表示/ひょうじ><用言代表表記:表示/ひょうじ><時制:非過去><格関係1:ガ:;><格解析結果:表示/ひょうじ:動1:ガ/N/;/1/0/1;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;デ/U/-/-/-/-><標準用言代表表記:表示/ひょうじ>
        表示 ひょうじ 表示 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:表示/ひょうじ カテゴリ:抽象物" <代表表記:表示/ひょうじ><カテゴリ:抽象物><正規化代表表記:表示/ひょうじ><漢字><かな漢字><名詞相当語><文頭><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        する する する 動詞 2 * 0 サ変動詞 16 基本形 2 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><とタ系連用テ形複合辞><付属>
        * -1D <文末><体言><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><裸名詞><提題受:30><主節><状態述語><正規化代表表記:;/;><主辞代表表記:;/;>
        + -1D <文末><体言><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><裸名詞><提題受:30><主節><状態述語><判定詞句><名詞項候補><先行詞候補><正規化代表表記:;/;><主辞代表表記:;/;><用言代表表記:;/;><CF_NOT_FOUND><節-区切><節-主辞><時制:非過去><解析連格:ガ><格解析結果:;/;:判0><標準用言代表表記:;/;>
        ; ; ; 名詞 6 普通名詞 1 * 0 * 0 "未知語:その他 品詞推定:特殊 疑似代表表記 代表表記:;/; 品詞変更:;-;-;-15-1-0-0" <未知語><品詞推定:特殊><疑似代表表記><代表表記:;/;><正規化代表表記:;/;><品詞変更:;-;-;-15-1-0-0-"未知語:その他 品詞推定:特殊 疑似代表表記 代表表記:;/;"><品曖-その他><記英数カ><英記号><記号><名詞相当語><文末><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        EOS
        """
    )
    doc = Document.from_knp(knp_text)
    # <格解析結果:表示/ひょうじ:動1:ガ/N/;/1/0/1;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;デ/U/-/-/-/->
    pas = doc.base_phrases[0].pas
    assert pas is not None
    assert pas.predicate.cfid == "表示/ひょうじ:動1"

    # ; ガ 表示する
    argument_base_phrase = doc.base_phrases[1]  # ;
    argument = pas.get_arguments("ガ", relax=False)[0]
    assert isinstance(argument, EndophoraArgument)
    assert argument.type == ArgumentType("N")
    assert argument.base_phrase == argument_base_phrase
    assert argument.phrase == argument_base_phrase.phrase
    assert argument.clause == argument_base_phrase.clause
    assert argument.sentence == argument_base_phrase.sentence
    assert argument.document == argument_base_phrase.document


def test_pas_case_analysis3() -> None:
    knp_text = textwrap.dedent(
        """\
        # S-ID:1 KNP:5.0-825c01b7 DATE:2021/10/04 SCORE:-8.40889
        * 1D <BGH:束の間/つかのま><文頭><時間><ガ><助詞><体言><判定詞><用言:判><係:連用><レベル:C><並キ:述:&ST:3.5&&&レベル:B><区切:3-5><ID:〜が><提題受:30><連用要素><連用節><状態述語><敬語:丁寧表現><正規化代表表記:束の間/つかのま><主辞代表表記:束の間/つかのま><並列類似度:1.258>
        + 1D <BGH:束の間/つかのま><文頭><時間><ガ><助詞><体言><判定詞><用言:判><係:連用><レベル:C><並キ:述:&ST:3.5&&&レベル:B><区切:3-5><ID:〜が><提題受:30><連用要素><連用節><状態述語><敬語:丁寧表現><節-機能-逆接:〜が><判定詞句><名詞項候補><先行詞候補><正規化代表表記:束の間/つかのま><主辞代表表記:束の間/つかのま><用言代表表記:束の間/つかのま><CF_NOT_FOUND><節-区切><節-主辞><時制:非過去><格解析結果:束の間/つかのま:判0><標準用言代表表記:束の間/つかのま>
        束の間 つかのま 束の間 名詞 6 普通名詞 1 * 0 * 0 "代表表記:束の間/つかのま カテゴリ:時間" <代表表記:束の間/つかのま><カテゴリ:時間><正規化代表表記:束の間/つかのま><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        です です だ 判定詞 4 * 0 判定詞 25 デス列基本形 27 NIL <かな漢字><ひらがな><活用語><付属>
        が が が 助詞 9 接続助詞 3 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:する/する><文末><サ変><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><敬語:丁寧表現><正規化代表表記:ゲーム/げーむ><主辞代表表記:ゲーム/げーむ>
        + -1D <BGH:する/する><文末><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><敬語:丁寧表現><サ変><正規化代表表記:ゲーム/げーむ><主辞代表表記:ゲーム/げーむ><用言代表表記:ゲーム/げーむ><節-区切><節-主辞><時制:非過去><主題格:一人称優位><格解析結果:ゲーム/げーむ:動0:ガ/U/-/-/-/-;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:ゲーム/げーむ>
        ゲーム げーむ ゲーム 名詞 6 普通名詞 1 * 0 * 0 "代表表記:ゲーム/げーむ ドメイン:レクリエーション カテゴリ:抽象物" <代表表記:ゲーム/げーむ><ドメイン:レクリエーション><カテゴリ:抽象物><正規化代表表記:ゲーム/げーむ><記英数カ><カタカナ><名詞相当語><サ変><自立><内容語><タグ単位始><文節始><固有キー><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        し し する 動詞 2 * 0 サ変動詞 16 基本連用形 8 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><とタ系連用テ形複合辞><付属>
        ます ます ます 接尾辞 14 動詞性接尾辞 7 動詞性接尾辞ます型 31 基本形 2 "代表表記:ます/ます" <代表表記:ます/ます><正規化代表表記:ます/ます><かな漢字><ひらがな><活用語><表現文末><付属>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
        EOS
        """
    )
    doc = Document.from_knp(knp_text)
    # <格解析結果:束の間/つかのま:判0>
    pas = doc.base_phrases[0].pas
    assert pas is not None
    assert pas.predicate.cfid == "束の間/つかのま:判0"
    assert len(pas._arguments) == 0


def test_pas_case_analysis4() -> None:
    knp_text = textwrap.dedent(
        """\
        # S-ID:1 KNP:5.0-25425d33 DATE:2022/07/06 SCORE:-17.49479
        * 1D <BGH:今朝/けさ><文頭><時間><強時間><体言><係:無格><区切:0-0><格要素><連用要素><正規化代表表記:今朝/けさ><主辞代表表記:今朝/けさ>
        + 1D <BGH:今朝/けさ><文頭><時間><強時間><体言><係:無格><区切:0-0><格要素><連用要素><名詞項候補><正規化代表表記:今朝/けさ><主辞代表表記:今朝/けさ><解析格:時間>
        今朝 けさ 今朝 名詞 6 時相名詞 10 * 0 * 0 "代表表記:今朝/けさ カテゴリ:時間" <代表表記:今朝/けさ><カテゴリ:時間><正規化代表表記:今朝/けさ><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
        * 3D <BGH:焼く/やく><時制:過去><連体修飾><用言:動><係:連格><レベル:B><区切:0-5><ID:（動詞連体）><連体節><動態述語><正規化代表表記:焼く/やく><主辞代表表記:焼く/やく>
        + 3D <BGH:焼く/やく><時制:過去><連体修飾><用言:動><係:連格><レベル:B><区切:0-5><ID:（動詞連体）><連体節><動態述語><正規化代表表記:焼く/やく><主辞代表表記:焼く/やく><用言代表表記:焼く/やく><節-区切:連体修飾><節-主辞><格関係0:時間:今朝><格関係3:ヲ:パン><格解析結果:焼く/やく:動1:ガ/U/-/-/-/-;ヲ/N/パン/3/0/1;ニ/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;時間/C/今朝/0/0/1><標準用言代表表記:焼く/やく>
        焼いた やいた 焼く 動詞 2 * 0 子音動詞カ行 2 タ形 10 "代表表記:焼く/やく ドメイン:健康・医学 自他動詞:自:焼ける/やける" <代表表記:焼く/やく><ドメイン:健康・医学><自他動詞:自:焼ける/やける><正規化代表表記:焼く/やく><かな漢字><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        * 3D <BGH:熱々/あつあつ><助詞><連体修飾><体言><係:ノ格><区切:0-4><正規化代表表記:熱々/あつあつ><主辞代表表記:熱々/あつあつ>
        + 3D <BGH:熱々/あつあつ><助詞><連体修飾><体言><係:ノ格><区切:0-4><名詞項候補><先行詞候補><係チ:非用言格解析||用言&&文節内:Ｔ解析格-ヲ><正規化代表表記:熱々/あつあつ><主辞代表表記:熱々/あつあつ>
        あつあつ あつあつ あつあつ 名詞 6 普通名詞 1 * 0 * 0 "代表表記:熱々/あつあつ カテゴリ:抽象物" <代表表記:熱々/あつあつ><カテゴリ:抽象物><正規化代表表記:熱々/あつあつ><かな漢字><ひらがな><名詞相当語><自立><内容語><タグ単位始><文節始><文節主辞>
        の の の 助詞 9 接続助詞 3 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:パン/ぱん><文末><体言><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><裸名詞><提題受:30><主節><状態述語><正規化代表表記:パン/ぱん><主辞代表表記:パン/ぱん>
        + -1D <BGH:パン/ぱん><文末><体言><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><裸名詞><提題受:30><主節><状態述語><判定詞句><名詞項候補><先行詞候補><正規化代表表記:パン/ぱん><主辞代表表記:パン/ぱん><用言代表表記:パン/ぱん><節-区切><節-主辞><時制:非過去><解析連格:ヲ><格解析結果:パン/ぱん:判0:ガ/U/-/-/-/-;ニ/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;時間/U/-/-/-/-;ノ/U/-/-/-/-><標準用言代表表記:パン/ぱん>
        パン ぱん パン 名詞 6 普通名詞 1 * 0 * 0 "代表表記:パン/ぱん ドメイン:料理・食事 カテゴリ:人工物-食べ物" <代表表記:パン/ぱん><ドメイン:料理・食事><カテゴリ:人工物-食べ物><正規化代表表記:パン/ぱん><記英数カ><カタカナ><名詞相当語><文末><表現文末><自立><内容語><タグ単位始><文節始><固有キー><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        EOS
        """
    )
    doc = Document.from_knp(knp_text)
    # <格解析結果:焼く/やく:動1:ガ/U/-/-/-/-;ヲ/N/パン/3/0/1;ニ/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;時間/C/今朝/0/0/1>
    pas = doc.base_phrases[1].pas
    assert pas is not None
    predicate = pas.predicate
    assert pas is not None

    assert predicate.cfid == "焼く/やく:動1"
    assert predicate.pas == pas
    assert predicate.base_phrase == doc.base_phrases[1]

    assert len(pas._arguments) == 2

    # パン ヲ 焼いた
    assert len(pas.get_arguments("ヲ", relax=False)) == 1
    argument = pas.get_arguments("ヲ", relax=False)[0]
    assert isinstance(argument, EndophoraArgument)
    assert argument.type == ArgumentType("N")
    assert argument.pas == pas
    assert argument.base_phrase == doc.base_phrases[3]  # パン

    # 今朝 時間 焼いた
    assert len(pas.get_arguments("時間", relax=False)) == 1
    argument = pas.get_arguments("時間", relax=False)[0]
    assert isinstance(argument, EndophoraArgument)
    assert argument.type == ArgumentType("C")
    assert argument.pas == pas
    assert argument.base_phrase == doc.base_phrases[0]  # 今朝


def test_pas_rel() -> None:
    doc_id = "w201106-0000060050"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    pas_list = doc.pas_list()
    assert len(pas_list) == 19

    pas = pas_list[1]
    assert (
        repr(pas) == "Pas(predicate=Predicate(text='トスを'), "
        "arguments={'ガ': [ExophoraArgument(exophora_referent=ExophoraReferent(text='不特定:人'), eid=0)], "
        "'ヲ': [EndophoraArgument(base_phrase=BasePhrase(index=0, text='コイン'), "
        "arg_type=<ArgumentType.CASE_HIDDEN: 'N'>)]})"
    )


def test_get_arguments_idempotency() -> None:
    doc_id = "w201106-0000060050"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    for pas in doc.pas_list():
        pas_before = id(pas)
        predicate_before = id(pas.predicate)
        arguments_before = id(pas._arguments)
        argument_list_before = [id(args) for args in pas._arguments.values()]
        each_argument_before = [id(arg) for args in pas._arguments.values() for arg in args]
        modes_before = id(pas.modes)
        _ = pas.get_all_arguments()
        pas_after = id(pas)
        predicate_after = id(pas.predicate)
        arguments_after = id(pas._arguments)
        argument_list_after = [id(args) for args in pas._arguments.values()]
        each_argument_after = [id(arg) for args in pas._arguments.values() for arg in args]
        modes_after = id(pas.modes)
        assert pas_before == pas_after
        assert predicate_before == predicate_after
        assert arguments_before == arguments_after
        assert argument_list_before == argument_list_after
        assert each_argument_before == each_argument_after
        assert modes_before == modes_after


def test_optional_case() -> None:
    original_log_level = logging.getLogger("rhoknp").level
    logging.getLogger("rhoknp").setLevel(logging.ERROR)
    knp_text = textwrap.dedent(
        """\
        # S-ID:w201106-0000085526-2 JUMAN:6.1-20101108 KNP:3.1-20101107 DATE:2011/06/21 SCORE:-98.90310 MOD:2018/02/18 MEMO:
        * 7D
        + 8D <NE:DATE:今日>
        今日 きょう 今日 名詞 6 時相名詞 10 * 0 * 0
        は は は 助詞 9 副助詞 2 * 0 * 0
        、 、 、 特殊 1 読点 2 * 0 * 0
        * 2D
        + 2D <rel type="ノ？" target="劇" sid="w201106-0000085526-1" id="8"/>
        役 やく 役 名詞 6 普通名詞 1 * 0 * 0
        を を を 助詞 9 格助詞 1 * 0 * 0
        * 4D
        + 4D <rel type="ヲ" target="役" sid="w201106-0000085526-2" id="1"/><rel type="時間" target="今日" sid="w201106-0000085526-2" id="0"/><rel type="ガ" target="私たち" sid="w201106-0000085526-1" id="0"/>
        決めて きめて 決める 動詞 2 * 0 母音動詞 1 タ系連用テ形 14
        * 4D
        + 4D <rel type="ノ" target="劇" sid="w201106-0000085526-1" id="8"/>
        場面 ばめん 場面 名詞 6 普通名詞 1 * 0 * 0
        ごと ごと ごと 接尾辞 14 名詞性名詞接尾辞 2 * 0 * 0
        に に に 助詞 9 格助詞 1 * 0 * 0
        * 7P
        + 8P <rel type="時間" target="今日" sid="w201106-0000085526-2" id="0"/><rel type="ガ" target="私たち" sid="w201106-0000085526-1" id="0"/><rel type="ニ" target="場面ごと" sid="w201106-0000085526-2" id="3"/>
        分かれ わかれ 分かれる 動詞 2 * 0 母音動詞 1 基本連用形 8
        、 、 、 特殊 1 読点 2 * 0 * 0
        * 7D
        + 6D <rel type="ノ？" target="劇" sid="w201106-0000085526-1" id="8"/>
        セリフ せりふ セリフ 名詞 6 普通名詞 1 * 0 * 0
        + 8D <rel type="ヲ" target="セリフ" sid="w201106-0000085526-2" id="5"/><rel type="時間" target="今日" sid="w201106-0000085526-2" id="0"/><rel type="ガ" target="私たち" sid="w201106-0000085526-1" id="0"/>
        覚え おぼえ 覚え 名詞 6 普通名詞 1 * 0 * 0 "品詞変更:覚え-おぼえ-覚える-2-0-1-8"
        と と と 助詞 9 格助詞 1 * 0 * 0
        * 7D
        + 8D <rel type="=" target="私たち" sid="w201106-0000085526-1" id="0"/>
        みんな みんな みんな 副詞 8 * 0 * 0 * 0
        で で で 助詞 9 格助詞 1 * 0 * 0
        * -1D
        + -1D <rel type="時間" target="今日" sid="w201106-0000085526-2" id="0"/><rel type="ガ" target="私たち" sid="w201106-0000085526-1" id="0"/><rel type="デ" target="みんな" sid="w201106-0000085526-2" id="7"/><rel type="デ" mode="？" target="なし"/><rel type="ヲ" target="セリフ" sid="w201106-0000085526-2" id="5"/><rel type="ヲ" mode="？" target="場面" sid="w201106-0000085526-2" id="3"/>
        合わせたり あわせたり 合わせる 動詞 2 * 0 母音動詞 1 タ系連用タリ形 15
        し し する 接尾辞 14 動詞性接尾辞 7 サ変動詞 16 基本連用形 8
        ました ました ます 接尾辞 14 動詞性接尾辞 7 動詞性接尾辞ます型 31 タ形 7
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        """
    )
    doc = Document.from_knp(knp_text)
    pas = doc.base_phrases[8].pas
    assert pas is not None
    assert len(pas.get_arguments("デ")) == 0
    arguments = pas.get_arguments("デ", relax=False, include_optional=True)
    assert {str(arg) for arg in arguments} == {"みんなで"}
    assert arguments[0].optional is True
    arguments_relaxed = pas.get_arguments("デ", relax=True, include_optional=True)
    assert {str(arg) for arg in arguments_relaxed} == {"みんなで"}
    logging.getLogger("rhoknp").setLevel(original_log_level)


def test_pas_relax() -> None:
    doc_id = "w201106-0000060560"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    pas = doc.base_phrases[18].pas
    assert pas is not None
    assert pas.predicate.text == "ご協力の"
    case = "ガ"
    args = sorted(
        pas.get_arguments(case, relax=True, include_nonidentical=True),
        key=lambda a: a.base_phrase.global_index if isinstance(a, EndophoraArgument) else 100,
    )
    assert len(args) == 4
    arg = args[0]
    assert isinstance(arg, EndophoraArgument)
    assert (arg.base_phrase.text, arg.base_phrase.global_index, arg.type) == ("ドクターを", 7, ArgumentType.OMISSION)
    arg = args[1]
    assert isinstance(arg, EndophoraArgument)
    assert (arg.base_phrase.text, arg.base_phrase.global_index, arg.type) == ("ドクターを", 11, ArgumentType.OMISSION)
    arg = args[2]
    assert isinstance(arg, EndophoraArgument)
    assert (arg.base_phrase.text, arg.base_phrase.global_index, arg.type) == ("ドクターの", 16, ArgumentType.OMISSION)
    arg = args[3]
    assert isinstance(arg, EndophoraArgument)
    assert (arg.base_phrase.text, arg.base_phrase.global_index, arg.type) == ("皆様", 17, ArgumentType.OMISSION)

    case = "ニ"
    args = pas.get_arguments(case, relax=True, include_nonidentical=True)
    arg = args[0]
    assert isinstance(arg, ExophoraArgument)
    assert (arg.exophora_referent.text, arg.eid, arg.type) == ("著者", 5, ArgumentType.EXOPHORA)
    arg = args[1]
    assert isinstance(arg, EndophoraArgument)
    assert (arg.base_phrase.text, arg.base_phrase.global_index, arg.type) == ("コーナーを", 14, ArgumentType.OMISSION)


def test_get_all_arguments() -> None:
    doc_id = "w201106-0000060050"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    pas = doc.pas_list()[3]
    all_arguments = pas.get_all_arguments()
    assert set(all_arguments.keys()) == {"ガ", "ヲ"}
    assert {str(arg) for arg in all_arguments["ガ"]} == {"不特定:人", "著者", "読者"}
    assert {str(arg) for arg in all_arguments["ヲ"]} == {"トスを"}
