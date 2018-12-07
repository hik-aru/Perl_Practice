#!C:\Perl64\bin\perl 

#-----------------------------------------------------------
# DBテーブルの登録内容表示CGI
# 2018/07/12
# Hikaru.Niida@sample.com
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
use loginDB;

sub show_table($$$);

my $q = new CGI;
print $q->header(-type => 'text/html', -charset=>'utf8');

# ENVファイル読み込み
my %env = loadEnv(); 


# log設定ファイルの読み込み
Log::Log4perl::init($env{LOG_CONFIG}); 


# log設定ファイルに定義したloggerを生成
my $logger = Log::Log4perl::get_logger("mylogger");
my $logMsg  = ''; 


# DBへ接続
my $dbh = loginDB($env{DB_USER}, $env{DB_PASS}, $env{DB_NAME}, $env{DB_HOST}, \$logMsg);
if(!$dbh){
    # 異状ログ出力
    $logger->debug("$logMsg"); 
    die("DB connection error"); 
}else{
    # 正常ログ出力
    $logger->debug("$logMsg");
}


#DBテーブルの登録情報表示
my $state = show_table($dbh, $env{TEMP_TABLE}, \$logMsg); 
if(!$state){
    #異状ログ出力
    $logger->debug("$logMsg"); 
    die( sprintf( 'DB execute failed ( %s )', $logMsg )); 
}else{
    #正常ログ出力
    $logger->debug("$logMsg");
}

exit;


#---------------------------------------------以下サブルーチン-------------------------------------------   
#----------------------------------------------------
#DBの登録内容表示
# 引数：$dbh：データベースハンドル
#       $env{TEMP_TABLE}：テーブル用テンプレートファイル
#       \$logMsg：ログメッセージ変数のリファレンス
#
# 戻り値：undef：登録失敗の場合
#         1：登録成功の場合
# 備考：
#----------------------------------------------------
sub show_table($$$){
    my ($dbh, $tmp_table, $ref_logMsg) = @_;
    
    #テンプレートを生成する。生成できなかった場合はログを出力
    my $template_table;
    eval{ $template_table = HTML::Template->new(filename => $tmp_table); };
    if($@){
        #ログメッセージ
	    $$ref_logMsg = sprintf('%s at line %s.', $@, __LINE__);
	    return (undef);
    }
    
    #文字コードの指定
    $dbh->do("set names utf8");
    
    #SQL文の準備
    my $sql ="select * from entry_info";
    my $sth = $dbh->prepare($sql);
    
    #エラーが出ればエラーメッセージを呼び出し元に返す
    if($sth->err()){ 
        $$ref_logMsg = sprintf( 'DB execute failed ( %s ) at line %s.', $sth->errstr(), __LINE__ );
        return (undef);
    }
    
    #SQL実行
    $sth->execute;
    
    #エラーが出れば
    if($sth->err()){
        #SQL実行エラーが出た場合、ログメッセージを呼び出し元に返して終了
        $$ref_logMsg = sprintf( 'DB execute failed ( %s ) at line %s.', $sth->errstr(), __LINE__ );
        return (undef);
    }else{
        #SQL実行成功の場合、ログメッセージを呼び出し元に返す
        $$ref_logMsg = sprintf('Displayed the table. sql:[%s] ', $sql);
    }
    
    #tableの登録情報取得
    my @loop_data = ();
    while(my @line = $sth->fetchrow_array){
        my %row_data;
        
        $row_data{NAME} = $line[0];
        $row_data{EMAIL} = $line[1];
        $row_data{SEX} = $line[2];
        $row_data{OLD} = $line[3];
        $row_data{FOOD1} = $line[4];
        $row_data{FOOD2} = $line[5];
        $row_data{FOOD3} = $line[6];
        $row_data{FOOD4} = $line[7];
        $row_data{MSG} = $line[8];
        
        push(@loop_data, \%row_data);
    }
    
    #登録情報画面の表示
    $template_table->param(DESC_TABLE => \@loop_data);
    print $template_table->output;
    
    #DB切断
    $sth->finish;
    $dbh->disconnect;
}
