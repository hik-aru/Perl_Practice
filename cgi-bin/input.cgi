#!C:\Perl64\bin\perl 

#-----------------------------------------------------------
# 入力画面用CGI
# 2018/06/25
# Hikaru.Niida@sample.com
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
use output_log;

my $q = new CGI;
my $submit = $q->param('submit') || 'default value';

print $q->header(-type => 'text/html', -charset=>'utf8');

#ENVファイル読み込み
my %env = loadEnv();

# log設定ファイルの読み込み
Log::Log4perl::init($env{LOG_CONFIG}); 

# log設定ファイルに定義したloggerを生成
my $logger = Log::Log4perl::get_logger("mylogger");
my $logMsg  = ''; 

#テンプレートを生成する。生成できなかった場合はログを出力。
my $template;
eval{ $template = HTML::Template->new(filename => $env{TEMP_INPUT}); };
if($@){
    #ログメッセージ
    $logMsg = sprintf("%s at line %s.", $@, __LINE__);
    
    #ログ出力
    $logger->debug("$logMsg");
}


if($submit eq "前のページへ戻る"){
    #確認画面から入力画面に遷移し、一度入力したフォーム内容は維持させる
    keepForm($q, $template);
    
    #入力画面表示
    print $template->output
    exit;
}else{
    #初期入力画面の表示
    #年齢フォーム作成
    my $oldlist = [
                    {VALUE => $env{DEF_OLD1}, CHECK => "", TEXT =>'0歳以上9歳未満'},
                    {VALUE => $env{DEF_OLD2}, CHECK => "", TEXT =>'10歳以上19歳未満'},
                    {VALUE => $env{DEF_OLD3}, CHECK => "", TEXT =>'20歳以上29歳未満'},
                    {VALUE => $env{DEF_OLD4}, CHECK => "", TEXT =>'30歳以上39歳未満'},
                    {VALUE => $env{DEF_OLD5}, CHECK => "", TEXT =>'40歳以上49歳未満'},
                    {VALUE => $env{DEF_OLD6}, CHECK => "", TEXT =>'50歳以上59歳未満'},
                    {VALUE => $env{DEF_OLD7}, CHECK => "", TEXT =>'60歳以上69歳未満'},
                    {VALUE => $env{DEF_OLD8}, CHECK => "", TEXT =>'70歳以上79歳未満'},
                    {VALUE => $env{DEF_OLD9}, CHECK => "", TEXT =>'80歳以上89歳未満'},
                    {VALUE => $env{DEF_OLD10}, CHECK => "", TEXT =>'90歳以上99歳未満'}
                  ];
    $template->param(OLD_FORM => $oldlist);
    
    #好きな食べ物フォーム作成
    my $foodlist = [
                    {VALUE => $env{DEF_FOOD1}, CHECK => ""},
                    {VALUE => $env{DEF_FOOD2}, CHECK => ""},
                    {VALUE => $env{DEF_FOOD3}, CHECK => ""},
                    {VALUE => $env{DEF_FOOD4}, CHECK => ""},
                   ];
    $template->param(FOOD_FORM => $foodlist);
    
    #入力画面表示
    print $template->output;
    exit;
}

