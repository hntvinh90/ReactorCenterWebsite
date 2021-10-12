// left justify for string
String.prototype.leftJustify = function(length, char){
    var fill = [];
    while (fill.length + this.length < length) {
        fill[fill.length] = char;
    }
    return fill.join('') + this;
}

// Print a element
function print_element(){
    var temp = $('body').html();
    $('body').html($('#id_for_printing').html());
    window.print();
    $('body').html(temp);
    $('#loading').modal("hide");
}
