#!C:\Perl64\bin\perl 
#use Data::Dumper:

#-----------------------------------------------------------
# 完了画面・CSV登録用CGI
# 2018/06/25
# Hikaru.Niida@sony.com
#----------------------------------------------------------- 
use strict;
use warnings;
use lib 'C:\Apache\Apache24\www\html\cgi-bin\lib';
use DBI;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use HTML::Template;
use Log::Log4perl;
use loadEnv;
use formCheck;
use loginDB;

sub register($$$);
sub complete($$$%);


my $q = new CGI;
print $q->header(-type => 'text/html', -charset=>'utf8');

# ENVファイル読み込み
my %env = loadEnv();  


# log設定ファイルの読み込み
Log::Log4perl::init($env{LOG_CONFIG}); 

# log設定ファイルに定義したloggerを生成
my $logger = Log::Log4perl::get_logger("mylogger");
my $logMsg  = ''; 


# 入力フォームのエラーチェック
my %form = formCheck($q, my $page=2);

if(!%form){
    #入力フォームチェックをパスすれば、DBにフォームデータを登録し完了画面を表示して終了
    
    # DBへ接続
    my $dbh = loginDB($env{DB_USER}, $env{DB_PASS}, $env{DB_NAME}, $env{DB_HOST}, \$logMsg);
    if(!$dbh){
        #DB接続失敗した場合、ログを出力
        # 異状ログ出力
        $logger->debug("$logMsg"); 
        die("DB connection error"); 
    }else{
        #DB接続成功した場合、ログを出力
        # 正常ログ出力
        $logger->debug("$logMsg");
    }
    
    # DBにフォームデータを登録する
    my $state = register($q, $dbh, \$logMsg); 
    if(!$state){
        #異状ログ出力
        $logger->debug("$logMsg"); 
        die( sprintf( "DB execute failed ( %s )", $logMsg )); 
    }else{
        #正常ログ出力
        $logger->debug("$logMsg");
    }
    
    #完了画面表示
    #定義されている全食品名を%foodに格納する
    my %food = ( food1 =>$env{DEF_FOOD1}, food2 =>$env{DEF_FOOD2}, food3 =>$env{DEF_FOOD3}, food4 =>$env{DEF_FOOD4} );
    
    #完了画面表示関数を呼び出す。エラーが出たらログ出力し終了
    my $tmp = complete($q, $env{TEMP_COMPLETE}, \$logMsg, %food);
    if(!$tmp){ $logger->debug("$logMsg"); };
    exit;
  
}else{
    #エラーに該当するメッセージをエラー画面に表示して終了

    #テンプレートを生成する。生成できなかった場合はログを出力。
    my $template_err;
    eval{ $template_err = HTML::Template->new(filename => $env{TEMP_ERROR}); };
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
    
    $template_err->param(ERR_MSG => $errList);
    #-------------------------------------------------------------------
    
    #エラーページ表示
    print $template_err->output;  
    exit;
}


#---------------------------------------------以下サブルーチン-------------------------------------------   
#----------------------------------------------------
#完了画面表示
# 引数：$q：cgiオブジェクト
#       $env{TEMP_COMPLETE}：完了画面用テンプレートファイル
#       \$logMsg：ログメッセージ変数のリファレンス
#       %food：食品名の一覧
#
# 戻り値：undef：テンプレートを開けない場合
# 備考：
#--------------------------------------------------
sub complete($$$%){
    my ($q, $tmp_comp, $ref_logMsg, %fd) = @_;
    
    #テンプレートを生成する。生成できなかった場合はログを出力
    my $template;
    eval{ $template = HTML::Template->new(filename => $tmp_comp); };
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
    $template->param(NAME => $name);
    $template->param(EMAIL => $email);
    $template->param(SEX => $sex);
    $template->param(OLD => $old);
    
    
    #選択された好きな食べ物名の文字連結を行う
    my @str;
    foreach my $foods(@ary){
        if($foods eq $fd{food1}){  # $fd{foods1} = 'ラーメン'
            push(@str, $foods);
        }elsif($foods eq $fd{food2}){  # $fd{foods2} = '焼肉'
            push(@str, $foods);
        }elsif($foods eq $fd{food3}){  # $fd{foods3} = 'カレー'
            push(@str, $foods);
        }elsif($foods eq $fd{food4}){  # $fd{foods4} = '牛丼'
            push(@str, $foods);
        }  
    }
    
    #カンマ区切りで食品名を連結する
    my $str = join(',', @str);
    
    #テンプレートに好きな食べ物のフォーム値設定
    $template->param(FOOD => $str);

    #テンプレートにメッセージのフォーム値設定
    $template->param(MSG => $msg);

    #完了画面表示
    print $template->output;
}

#----------------------------------------------------
#DB登録
# 引数：$q：cgiオブジェクト
#       $dbh：データベースハンドル
#       \$logMsg：ログメッセージ変数のリファレンス
#
# 戻り値：undef：テンプレートを開けない場合
# 備考：
#----------------------------------------------------
sub register($$$){
	my ($q, $dbh, $ref_logMsg) = @_;
	
    #名前・メアド・性別・年齢・好きな食べ物・メッセージのフォーム値取得
    my $name = $q->param('name') || 'default value';
    my $email = $q->param('email') || 'default value';
    my $sex = $q->param('sex') || 'default value';
    my $old = $q->param('old') || 'default value';
    my @ary = $q->multi_param('ary');
    my $msg = $q->param('msg') || 'default value';
    
    #好きな食べ物データの前処理
    my $foodsName_csv = join(',', @ary);
   
    #メッセージデータの前処理
    my $msg_str = join('|', split(/<br>/, $msg));
    
    #文字コードの指定
    $dbh->do("set names utf8");
    
    #SQL文の準備
    my $sql = "insert into entry_info values(?, ?, ?, ?, ?, ?, ?, ?, ?)";
    my $sth = $dbh->prepare($sql);
    
    #エラーが出ればエラーメッセージを呼び出し元に返す
    if($sth->err()){ 
        $$ref_logMsg = sprintf( 'DB execute failed ( %s ) at line %s.', $sth->errstr(), __LINE__ );
        return (undef);
    }
    
    #SQL実行
    $sth->execute($name,$email,$sex,$old,$ary[0],$ary[1],$ary[2],$ary[3],$msg);
    
    if($sth->err()){ 
        #SQL実行エラーが出た場合、ログメッセージを呼び出し元に返す
        $$ref_logMsg = sprintf( 'DB execute failed ( %s ) at line %s.', $sth->errstr(), __LINE__ );
        return (undef);
    }else{
        #SQL実行成功の場合、ログメッセージを呼び出し元に返す
        $$ref_logMsg = "Registration Successful. sql:[$sql]";
        
        #DB切断
        $sth->finish;
        $dbh->disconnect;
    }
}

