
package output_log;

#use strict;
use warnings;
use DateTime;
use base Exporter;
our(@EXPORT) = qw(output_log);

#----------------------------------------------------
#エラーログ出力
# 引数：$msg：メッセージ
#
# 戻り値：なし
# 備考：
#----------------------------------------------------
sub output_log($$$){
    my ($msg, $fn, $row) = @_;
    chomp($msg);
    
    #日付取得
    my $dt = DateTime->now;
    my $ymd = $dt->ymd('/');
    my $hms = $dt->hms;
    my $date_str = "$ymd ".$hms;
    
    #ログファイル名
    my $filename = 'C:\Apache\Apache24\www\html\cgi-bin\logs\log.log';
    
    open(LOG, ">>", "$filename") or die "Can't open log.txt .";
    printf(LOG "(%s) %s: %s(line:%s)\n", $date_str, $fn, $msg, $row);
    close(LOG);
}

1;