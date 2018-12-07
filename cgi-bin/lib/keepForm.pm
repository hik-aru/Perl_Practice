
package keepForm;

#use strict;
use warnings;
use loadEnv;
use base Exporter;
our(@EXPORT) = qw(keepForm);

my %env = loadEnv();

#----------------------------------------------------
#フォーム状態維持
# 引数：$q：cgiオブジェクト
#       $template：htmlテンプレート(入力画面)
#
# 戻り値：なし
# 備考：
#--------------------------------------------------
sub keepForm($$){
    my ($q, $template) = @_;
    
    #名前・メアド・性別・年齢・好きな食べ物・メッセージのフォーム値取得
    my $name = $q->param('name');
    my $email = $q->param('email');
    my $sex = $q->param('sex') || 'default value';
    my $old = $q->param('old') || 'default value';
    my @ary = $q->multi_param('ary');
    my $msg = $q->param('frmMsg');
    
    #テンプレートに名前・メアド・メッセージのフォーム値設定
    $template->param(NAME => $name);
    $template->param(EMAIL => $email);        
    $template->param(MSG => $msg);
    
    #テンプレートに性別のフォーム値設定
    if($sex eq $env{DEF_MAN}){
        $template->param(MAN => $env{FRM_CHECK});
    }elsif($sex eq $env{DEF_WOMAN}){
        $template->param(WOMAN => $env{FRM_CHECK});
    }
    
    #年齢の選択状態保持
    my ($ck1, $ck2, $ck3, $ck4, $ck5, $ck6, $ck7, $ck8, $ck9, $ck10) = (0, 0, 0, 0, 0, 0, 0, 0, 0);
     
    if($old eq $env{DEF_OLD1}){
        $ck1 = $env{FRM_SELECT};
    }elsif($old eq $env{DEF_OLD2}){
        $ck2 = $env{FRM_SELECT};
    }elsif($old eq $env{DEF_OLD3}){
        $ck3 = $env{FRM_SELECT};
    }elsif($old eq $env{DEF_OLD4}){
        $ck4 = $env{FRM_SELECT};
    }elsif($old eq $env{DEF_OLD5}){
        $ck5 = $env{FRM_SELECT};
    }elsif($old eq $env{DEF_OLD6}){
        $ck6 = $env{FRM_SELECT};
    }elsif($old eq $env{DEF_OLD7}){
        $ck7 = $env{FRM_SELECT};
    }elsif($old eq $env{DEF_OLD8}){
        $ck8 = $env{FRM_SELECT};
    }elsif($old eq $env{DEF_OLD9}){
        $ck9 = $env{FRM_SELECT};
    }else{
        $ck10 = $env{FRM_SELECT};
    }
    #年齢フォーム作成
    my $oldlist = [
                    {VALUE => $env{DEF_OLD1}, CHECK => "$ck1", TEXT =>'0歳以上9歳未満'},
                    {VALUE => $env{DEF_OLD2}, CHECK => "$ck2", TEXT =>'10歳以上19歳未満'},
                    {VALUE => $env{DEF_OLD3}, CHECK => "$ck3", TEXT =>'20歳以上29歳未満'},
                    {VALUE => $env{DEF_OLD4}, CHECK => "$ck4", TEXT =>'30歳以上39歳未満'},
                    {VALUE => $env{DEF_OLD5}, CHECK => "$ck5", TEXT =>'40歳以上49歳未満'},
                    {VALUE => $env{DEF_OLD6}, CHECK => "$ck6", TEXT =>'50歳以上59歳未満'},
                    {VALUE => $env{DEF_OLD7}, CHECK => "$ck7", TEXT =>'60歳以上69歳未満'},
                    {VALUE => $env{DEF_OLD8}, CHECK => "$ck8", TEXT =>'70歳以上79歳未満'},
                    {VALUE => $env{DEF_OLD9}, CHECK => "$ck9", TEXT =>'80歳以上89歳未満'},
                    {VALUE => $env{DEF_OLD10}, CHECK => "$ck10", TEXT =>'90歳以上99歳未満'}
                  ];
    $template->param(OLD_FORM => $oldlist);    
    
    #好きな食べ物のチェック状態保持
    foreach my $foods(@ary){
        if($foods eq $env{DEF_FOOD1}){
            $ck1 = $env{FRM_CHECK};
        }elsif($foods eq $env{DEF_FOOD2}){
            $ck2 = $env{FRM_CHECK};
        }elsif($foods eq $env{DEF_FOOD3}){
            $ck3 = $env{FRM_CHECK};
        }elsif($foods eq $env{DEF_FOOD4}){
            $ck4 = $env{FRM_CHECK};
        }
    }
    #好きな食べ物フォームのループリスト
    my $foodlist = [
                    {VALUE => $env{DEF_FOOD1}, CHECK => "$ck1"},
                    {VALUE => $env{DEF_FOOD2}, CHECK => "$ck2"},
                    {VALUE => $env{DEF_FOOD3}, CHECK => "$ck3"},
                    {VALUE => $env{DEF_FOOD4}, CHECK => "$ck4"},
                   ];
    $template->param(FOOD_FORM => $foodlist);
}

1;