#!C:\Perl64\bin\perl 
#use Data::Dumper:

#-----------------------------------------------------------
# 確認画面用CGI
# 2018/06/25
# Hikaru.Niida@sample.com
#
#----------------------------------------------------------- 
use strict;
use warnings;
use lib 'C:\Apache\Apache24\www\html\cgi-bin\lib';
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use HTML::Template;
use Log::Log4perl;
use keepForm;
use loadEnv;
use formCheck;

sub confirm($$$%);


my $q = new CGI;
print $q->header(-type => 'text/html', -charset=>'utf8');

#ENVファイル読み込み
my %env = loadEnv(); 


# log設定ファイルの読み込み
Log::Log4perl::init($env{LOG_CONFIG}); 

# log設定ファイルに定義したloggerを生成
my $logger = Log::Log4perl::get_logger("mylogger");
my $logMsg  = ''; 

# 入力フォームのエラーチェック
my %form = formCheck($q, my $page=1); 
	
if(!%form){
    #入力フォームチェックをパスすれば、確認画面を表示して終了
    
    #定義されている全食品名を%foodに格納する
    my %food = ( food1 =>$env{DEF_FOOD1}, food2 =>$env{DEF_FOOD2}, food3 =>$env{DEF_FOOD3}, food4 =>$env{DEF_FOOD4} );
    
    #確認画面表示関数を呼び出す。エラーが出たらログ出力し終了
    my $tmp = confirm($q, $env{TEMP_CONFIRM}, \$logMsg, %food);
    if(!$tmp){ $logger->debug("$logMsg"); };
    
    exit;
}else{
    #エラーに該当するメッセージを入力画面に書き込み、一度入力されたデータはフォーム欄に保持する。

    #テンプレートを生成する。生成できなかった場合はログを出力
    my $template;
    eval{ $template = HTML::Template->new(filename => $env{TEMP_INPUT}); };
    if($@){
        #ログメッセージ
        $logMsg = sprintf("%s at line %s.", $@, __LINE__);
	    
	    #ログ出力
	    $logger->debug("$logMsg");
    }
    #-------------------------エラーメッセージ書き込み------------------
    my $errList = [
                    {VALUE => $form{frmerr_name}},
                    {VALUE => $form{frmerr_sex}},
                    {VALUE => $form{frmerr_old}},
                    {VALUE => $form{frmerr_food}},
                    {VALUE => $form{frmerr_email}}
                   ];
    
    $template->param(ERR_MSG => $errList);
    #-------------------------------------------------------------------
    
    #フォーム欄の状態保持 
    keepForm($q, $template); 
    
    #エラーを追記した入力画面表示
    print $template->output;  
    exit;
}



#---------------------------------------------以下サブルーチン-------------------------------------------        
#----------------------------------------------------
#確認画面表示
# 引数：$q：cgiオブジェクト
#       $env{TEMP_CONFIRM}：確認画面用テンプレートファイル
#       \$logMsg：ログメッセージ変数のリファレンス
#       %food：食品名の一覧
#
# 戻り値：undef：テンプレートを生成できない場合
# 備考：
#--------------------------------------------------
sub confirm($$$%){
    my ($q, $tmp_cfm, $ref_logMsg, %fd) = @_;
    
    #テンプレートを生成。生成できなかった場合はログメッセージを呼び出し元に返す。
    my $template_cfm;
    eval{ $template_cfm = HTML::Template->new(filename => $tmp_cfm); };
    if($@){
        #ログメッセージ
 	    $$ref_logMsg = sprintf('%s at line %s.', $@, __LINE__);
 	    return (undef);
    }
   
    #名前・メアド・性別・年齢・好きな食べ物・メッセージのフォーム値取得
    my $name = $q->param('name');
    my $email = $q->param('email');
    my $sex = $q->param('sex');
    my $old = $q->param('old');
    my @ary = $q->multi_param('ary');
    my $msg = $q->param('msg');
    
    #テンプレートに名前・メアド・性別・年齢のフォーム値設定
    $template_cfm->param(NAME => $name);
    $template_cfm->param(EMAIL => $email);    
    $template_cfm->param(SEX => $sex);
    $template_cfm->param(OLD => $old);
    
    #テンプレートに好きな食べ物のフォーム値設定
    #ハッシュの配列
    my @loop_data = ();
    
    #好きな食べ物名が含まれていれば、その名前をハッシュリファレンスとして配列に追加する。
    foreach my $line(@ary){
        my %food_data;
        
        if($line eq $fd{food1}){            # $fd{foods1} = 'ラーメン'
            $food_data{VALUE} = $line;
            push(@loop_data, \%food_data);
        }elsif($line eq $fd{food2}){        # $fd{foods2} = '焼肉'
            $food_data{VALUE} = $line;
            push(@loop_data, \%food_data);
        }elsif($line eq $fd{food3}){        # $fd{foods3} = 'カレー'
            $food_data{VALUE} = $line;
            push(@loop_data, \%food_data);
        }elsif($line eq $fd{food4}){        # $fd{foods4} = '牛丼'
            $food_data{VALUE} = $line;
            push(@loop_data, \%food_data);
        }  
    }
    #好きな食べ物名のフォーム値設定
    $template_cfm->param(FOOD_HIDDEN => \@loop_data);

    #選択された好きな食べ物名の文字連結を行う
    my $str;
    for (my $i=0; $i<=$#loop_data; $i++){
        #ハッシュリファレンス取得
        my $food = $loop_data[$i];
        
        #配列の先頭要素の場合は、カンマを末尾に連結しない
        if(!$i == 0){
            $str = $str.",";
        }
        
        #カンマ区切りで食品名を連結する
        $str = $str.%$food{VALUE};
    }
    $template_cfm->param(FOOD => $str);
    
    
    
    #改行文字でtextareaの文字列を分割する
    my @line = split(/\x0D\x0A/, $msg);
    
    #html上で改行して表示させるために、末尾に<br>タグを連結する。
    my $str_msg;
    for(my $i=0; $i<=$#line; $i++){
        $str_msg = $str_msg.$line[$i]."<br>";
    }
    
    #テンプレートにメッセージのフォーム値設定
    $template_cfm->param(MSG => $str_msg);
    
    #メッセージのフォーム状態を維持させるために、無加工のメッセージ値を設定
    $template_cfm->param(FRMMSG => $msg);
    
    
    #確認画面表示
    print $template_cfm->output;
}


