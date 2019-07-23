function show(shown, hidden, hidden2) {
        document.body.scrollTop = document.documentElement.scrollTop = 400;
        document.getElementById(shown).style.display='block';
        document.getElementById(hidden).style.display='none';
        document.getElementById(hidden2).style.display='none';
        return false;
    }
function showall(shown, hidden, hidden2) {
    document.getElementById(shown).style.display='block';
    document.getElementById(hidden).style.display='block';
    document.getElementById(hidden2).style.display='block';
    return false;
}