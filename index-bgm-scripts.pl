#!/usr/bin/env perl

use strict; use warnings;
use File::Basename;

# 将 https://github.com/bangumi/scripts 中的脚本索引更新到本repo的README.md
# 执行时PWD应为那个repo的work tree

my @new_script_list = ();
for(`grep -Rin '^##'`) {
    if (/ ^ ([^\/]+) (?:\/) .* \[ (.*) \] \( .* \) /ix) {
        my $username = $1;
        my $script = $2;
        (my $link_id = $2) =~ s{\s+}{-}g;
        $link_id =~ tr/A-Z/a-z/;
        $link_id =~ s{[+]}{}g;
        push @new_script_list, "- [$username / $script](https://github.com/bangumi/scripts/tree/master/$username#$link_id)";
    }
}

@new_script_list = sort @new_script_list;

my $readme_fn = "${\(dirname $0)}/README.md";
my @old_lines;
my $readme;

{
    open my $readme, $readme_fn or die "error opening $readme_fn for read";
    @old_lines = <$readme>;
    close $readme;
    @old_lines or die "failed to find userscripts.\nthis script should be executed within https://github.com/bangumi/scripts repo.\n";
}

{
    open my $readme, ">", $readme_fn or die "error opening $readme_fn for write";
    for (@old_lines) {
        my $in_script_list = /bangumi\/scripts START/ .. /bangumi\/scripts END/;
        if ($in_script_list and /bangumi\/scripts START/) {
            print $readme "<!--bangumi/scripts START-->\n";
            for (@new_script_list) { print $readme "    $_\n"; }
            print $readme "<!--bangumi/scripts END-->\n";
        } elsif (!$in_script_list) {
            print $readme $_;
        }
    }
    close $readme;
}

print "updated $readme_fn\n";
