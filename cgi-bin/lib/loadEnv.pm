
package loadEnv;

#use strict;
use warnings;
use Log::Log4perl;
use base Exporter;
our(@EXPORT) = qw(loadEnv);

our $env_file = 'C:\Apache\Apache24\www\html\cgi-bin\env\constant.env';
our $err_file = 'C:\Apache\Apache24\www\html\cgi-bin\tmplt\error.tmpl';

#----------------------------------------------------
#ENVデータのハッシュ化
# 引数：なし
#
# 戻り値：ENVデータ
#   %env：ENVデータのハッシュ
# 備考：
#----------------------------------------------------
sub loadEnv(){
    if(open(IN, "<", "$env_file")){
        #envファイルのデータを1行ずつ配列に格納する
        my @list = <IN>;
        close(IN);
         
        my %env;
        foreach my $line(@list){
            chomp $line;
            if($line){
                
                if($line !~ /^\S+\s+.*$/){
                    #envファイルの定義が規定のフォーマットでなければ、エラー画面表示して終了
                    $template_err->param(ERROR => "The data format of the env-file is wrong.");
                    print $template_err->output;
                    exit;   
                }
                
                #読み込んだ行が空行でなければ、タブ区切りで値を分割しハッシュに格納する
                my ($key, $value) = split(/\s+/, $line);
                $env{$key} = $value;
            }
        }     
        return %env;
    }else{
        #envファイルを開けなければ、エラー画面表示して終了
        $template_err->param(ERROR => "Can't open env file.");
        print $template_err->output;
        exit;
    }
}

1;