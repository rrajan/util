awk '
BEGIN{
    f1 = "ObjectId"
    f2 = "ISODate"
    b1s = "\("
    b1e = "\)"
    TABS="    "
}
{

    x = gsub(/\t/, TABS)
    if ($0 ~ f1) {
        x=gsub(f1, "")
        x=gsub(/\(/, " ")
        x=gsub(/\)/, " ")
    }
    if ($0 ~ f2) {
        x=gsub(f2, "")
        x=gsub(/\(/, " ")
        x=gsub(/\)/, " ")
    }

    print $0

}'
