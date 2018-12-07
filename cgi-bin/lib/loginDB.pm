#!C:\Perl64\bin\perl 

package loginDB;

#use strict
use warnings;
use base Exporter;
our(@EXPORT) = qw(loginDB);

#----------------------------------------------------
#DB接続
# 引数：$env{DB_USER}：ログイン ユーザー名
#       $env{DB_PASS}：ログイン パスワード
#       $env{DB_NAME}：データベース名
#       $env{DB_HOST}：ホスト名
#       \$logMsg：ログメッセージ変数のリファレンス
#
# 戻り値：undef：接続失敗した場合
#         $dbh：データベースハンドル
# 備考：
#----------------------------------------------------
sub loginDB($$$$$){
    my ($user, $pass, $database, $hostname, $ref_logMsg) = @_;
    
    my $dsn = "DBI:mysql:database=$database;host=$hostname";

    my $dbh = DBI->connect($dsn, $user, $pass);
    if(!$dbh) {
        #DB接続失敗した場合、ログメッセージを呼び出し元に返す
        $$ref_logMsg = sprintf( "DB connection error【%s】at line %s.", $DBI::errstr, __LINE__);
        return (undef);
    }else{
        #DB接続成功した場合、ログメッセージとデータベースハンドルを呼び出し元に返す
        $$ref_logMsg = sprintf("Login Successful. [User:%s]", $user);
        return $dbh;
    }
}

1;