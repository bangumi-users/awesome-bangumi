#!/usr/bin/env perl

# 生成 https://github.com/bangumi/scripts 中的脚本索引
# 执行时PWD应为那个repo的work tree
for(`grep -Rin '^##'`) {
    if (/ ^ ([^\/]+) (?:\/) .* \[ (.*) \] \( .* \) /ix) {
        my $username = $1;
        my $script = $2;
        (my $link_id = $2) =~ s{\s+}{-}g;
        $link_id =~ tr/A-Z/a-z/;
        $link_id =~ s{[+]}{}g;
        print "- [$script by $username](https://github.com/bangumi/scripts/tree/master/$username#$link_id)\n";
    }
}
