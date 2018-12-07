
package formCheck;

#use strict;
use warnings;
use loadEnv;
use base Exporter;
our(@EXPORT) = qw(formCheck);

my %env = loadEnv();

#----------------------------------------------------
#入力フォームのエラーチェック
# 引数：$q：cgiオブジェクト
#       $page：チェックしているページの識別値
#
# 戻り値：%form：エラーチェック結果
# 備考：
#       ページ識別値 1: 入力画面
#       ページ識別値 2: 完了画面
#--------------------------------------------------
sub formCheck($$){
    my ($q, $page) = @_;
    
    #名前・メアド・性別・年齢・好きな食べ物・メッセージのフォーム値取得
    my $name = $q->param('name');
    my $email = $q->param('email');
    my $sex = $q->param('sex');
    my $old = $q->param('old');
    my @ary = $q->multi_param('ary');
    my $msg = $q->param('msg');
    
    #入力チェックの結果を格納するハッシュ変数
    my %form;
    
    #名前フォーム欄のチェック
    if(!$name && $page == 1){
        $form{'frmerr_name'} = $env{ERR_MSG_RQ_NAME};
    }elsif(!$name && $page == 2){
        $form{'frmerr_name'} = $env{ERR_MSG_PM_NAME};
    }
    
    #性別フォーム欄のチェック
    if(!$sex && $page == 1){
        $form{'frmerr_sex'} = $env{ERR_MSG_RQ_SEX};
    }elsif(!$sex && $page == 2){
        $form{'frmerr_sex'} = $env{ERR_MSG_PM_SEX};
    }
    
    #年齢フォーム欄のチェック
    if(!$old && $page == 1){
        $form{'frmerr_old'} = $env{ERR_MSG_RQ_OLD};
    }elsif(!$old && $page == 2){
        $form{'frmerr_old'} = $env{ERR_MSG_PM_OLD};
    }
    
    #好きな食べ物フォーム欄のチェック
    my $checked=0;
    foreach $foods(@ary){    
        if($foods eq $env{DEF_FOOD1}){
            $checked = 1;
        }elsif($foods eq $env{DEF_FOOD2}){
            $checked = 1;
        }elsif($foods eq $env{DEF_FOOD3}){
            $checked = 1;
        }elsif($foods eq $env{DEF_FOOD4}){
            $checked = 1;
        }      
    }
    if($checked != 1 && $page == 1){
        $form{'frmerr_food'} = $env{ERR_MSG_RQ_FOOD};
    }elsif($checked != 1 && $page == 2){
        $form{'frmerr_food'} = $env{ERR_MSG_PM_FOOD};
    }
    
    #メールアドレスフォーム欄のチェック
    if(defined $email && $email =~ /^([a-z0-9\-_]+)(\.[a-z0-9]+)*@([a-z0-9]+)\.?[a-z]+$/i ||
       defined $email && $email =~ /^([a-z0-9\-_]+)(\.[a-z0-9]+)*@([a-z0-9]+)(\.[a-z0-9]+)\.?[a-z]+$/i){
    }elsif($page == 1){
        $form{'frmerr_email'} = $env{ERR_MSG_EMAIL};
    }elsif($page == 2){
        $form{'frmerr_email'} = $env{ERR_MSG_PM_EMAIL};
    }
    
    return %form;    
}

1;