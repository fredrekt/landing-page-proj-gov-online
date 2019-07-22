var searchColumn = 0,
    input = document.getElementById("searchPerm");

$("#searchByChoices .dropdown-item").click(function(){
    var type = $(this).html();
    if(type == "Permit Number") {
        $("#searchPerm").attr("type", "number");
    } else {
        $("#searchPerm").attr("type", "text");
    }
    switch(type) {
        case "Permit Number":
            searchColumn = 1;
            break;
        case "Applicant":
            searchColumn = 2;
            break;
        case "Business":
            searchColumn = 3;
            break;
        case "City":
            searchColumn = 4;
            break;
        default: 
            searchColumn = 0;
            break;
    }

    $("#searchBy span").html($(this).html());
    $("#searchPerm").select();
});
 
function doSearch(val) {
    val = val.toLowerCase();
    $("#permits tbody tr").each(function(){
        var content;
        if(searchColumn == 0) { 
            content = $(this).html().toLowerCase();
        } else {
            content = $(this).children(`td:nth-child(${searchColumn})`).html().toLowerCase();
        }

        if(!content.includes(val)) {
            $(this).hide();
        } else {
            $(this).show();
        }
    });
}