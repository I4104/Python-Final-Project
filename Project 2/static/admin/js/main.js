// For search and load table
$("#search").bind('input', function() {
    var search = $("#search").val();
    var _page = parseInt($("#page").text());
    if (search != '') {
        $("#product").load("execute/load/product.php?page=" + _page + "&search=" + search);
        $("#users").load("execute/load/users.php?page=" + _page + "&search=" + search);
        $("#orders").load("execute/load/orders.php?page=" + _page + "&search=" + search);    
        $("#category").load("execute/load/category.php?page=" + _page + "&search=" + search);    
    } else {
        load(parseInt($("#page").text()));   
    }
});

$("#search_ship").bind('input', function() {
    var search = $("#search_ship").val();
    var _page = parseInt($("#page_ship").text());
    if (search != '') {
        $("#page_ship").load("execute/load/orders.php?load=ship&page=" + _page + "&search=" + search);    
    } else {
        load(parseInt($("#page").text()));   
    }
});

$("#search_done").bind('input', function() {
    var search = $("#search_done").val();
    var _page = parseInt($("#page_done").text());
    if (search != '') {  
        $("#page_done").load("execute/load/orders.php?load=done&page=" + _page + "&search=" + search);    
    } else {
        load(parseInt($("#page").text()));   
    }
});


$("#price").bind('input', function() {
    var price = $("#price").val();
    $("#price").val(new Intl.NumberFormat('vn-VN').format(price.replaceAll(".", "")));
    
});

function pre() {
    var _page = parseInt($("#page").text());
    if (_page > 1) {
        load(_page - 1);
    } else {
        return;   
    }
}

function next() {
    var _page = parseInt($("#page").text());
    load(eval(_page + 1));
}


function next_ship() {
    var _page = parseInt($("#page").text());
    load(eval(_page + 1));
}

function pre_ship() {
    var _page = parseInt($("#page").text());
    if (_page > 1) {
        load(_page - 1);
    } else {
        return;   
    }
}

function next_ship() {
    var _page = parseInt($("#page_ship").text());
    load_ship(eval(_page + 1));
}

function pre_done() {
    var _page = parseInt($("#page_ship").text());
    if (_page > 1) {
        load_ship(_page - 1);
    } else {
        return;   
    }
}

function next_done() {
    var _page = parseInt($("#page_done").text());
    load_done(eval(_page + 1));
}

function pre_done() {
    var _page = parseInt($("#page_done").text());
    if (_page > 1) {
        load_done(_page - 1);
    } else {
        return;   
    }
}


load(1);
load_cate();
load_ship(1);
load_done(1);

setInterval(function() { 
    load(parseInt($("#page").text())); 
    load_ship(parseInt($("#page_ship").text()));
    load_done(parseInt($("#page_done").text()));
}, 5000); 

function load_ship(_page) {
    $("#orders_ship").load("execute/load/orders.php?load=ship&page=" + _page);
}

function load_done(_page) {
    $("#orders_done").load("execute/load/orders.php?load=done&page=" + _page);
}

function load_cate() {
    $("#category_select").load("execute/load/category.php?load=select");
}

function load(_page){
    $("#logs").load("execute/load/logs.php?page=" + _page);
    $("#product").load("execute/load/product.php?page=" + _page);
    $("#users").load("execute/load/users.php?page=" + _page);
    $("#orders").load("execute/load/orders.php?page=" + _page);
    $("#category").load("execute/load/category.php?page=" + _page);
    $("#category").load("execute/load/category.php?page=" + _page);
    $("#code").load("execute/load/code.php");
}

// For codes
$("#add_new_code").on('submit', function (e) {
    e.preventDefault();
    $.ajax({
        url: 'execute/handler/code.php?action=add',
        type: 'POST',
        data: $(this).serialize(),
        success: function(data) {
            var obj = JSON.parse(data);
            load(parseInt($("#page").text()));
            swal(obj.title, obj.message, obj.type).then(function() {
                if (obj.type == "success") {
                    $('#add_code').modal('hide');
                    $("#code").val("");
                    $("#sale").val("");
                }
            });
        }
    });
});

function code_delete(id) {
    $.ajax({
        url: 'execute/handler/code.php?action=delete&id=' + id,
        type: 'GET',
        success: function(data) {
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type);
            load(parseInt($("#page").text()));
        }
    });
}

function code_edit(item) {
    var code = $("#" + item).attr("data-code");
    var sale = $("#" + item).attr("data-sale");
    
    $("#e_code").val(code);
    $("#e_sale").val(sale);
    
    $("#edit_code").modal("show");
}

$("#code_edit").on('submit', function(e) {
    e.preventDefault();
    $.ajax({
        url: 'execute/handler/code.php?action=edit',
        type: 'POST',
        data: $(this).serialize(),
        success: function(data) {
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type).then(function() {
                if (obj.type == "success") {
                    $('#edit_code').modal('hide');
                    $("#e_code").val("");
                    $("#e_sale").val("");
                }
            });
            load(parseInt($("#page").text()));
        }
    });
});


// For product
$("#hang_check").on('change', function() {
    if ($(this).is(':checked')) {
        $("#hang").prop("disabled", true);
        $("#load_hang").append('<select name="hang" id="current_hang" class="form-control"></select>');
        $("#current_hang").load("execute/load/category.php?load=hang");
    } else {
        $("#hang").prop("disabled", false);
        $("#current_hang").remove();
    }
});

$("#dongmay_check").on('change', function() {
    if ($(this).is(':checked')) {
        $("#dongmay").prop("disabled", true);
        $("#load_dongmay").append('<select name="dongmay" id="current_dongmay" class="form-control"></select>');
        $("#current_dongmay").load("execute/load/category.php?load=dongmay");
    } else {
        $("#dongmay").prop("disabled", false);
        $("#current_dongmay").remove();
    }
});

$("#phankhuc_check").on('change', function() {
    if ($(this).is(':checked')) {
        $("#phankhuc").prop("disabled", true);
        $("#load_phankhuc").append('<select name="phankhuc" id="current_phankhuc" class="form-control"></select>');
        $("#current_phankhuc").load("execute/load/category.php?load=phankhuc");
    } else {
        $("#phankhuc").prop("disabled", false);
        $("#current_phankhuc").remove();
    }
});

$("#add_product").on('submit', function(e) {
    e.preventDefault();
    $.ajax({
        url: 'execute/handler/product.php?action=add',
        type: 'POST',
        data: $(this).serialize(),
        success: function(data) {
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type);
            if (obj.type == "success") {
                $("#product_name").val("");
                $("#category_select").val("");
                
                $("#hang").val("");
                $("#hang_check").prop("checked", false);
                $("#hang").prop("disabled", false);
                $("#current_hang").remove();
                
                $("#dongmay").val("");
                $("#dongmay_check").prop("checked", false);
                $("#dongmay").prop("disabled", false);
                $("#current_dongmay").remove();
                
                $("#phankhuc").val("");
                $("#phankhuc_check").prop("checked", false);
                $("#phankhuc").prop("disabled", false);
                $("#current_phankhuc").remove();
                
                $("#price").val("");
                $("#sale").val("");
                $('#add_new_product').modal('hide');
                load(parseInt($("#page").text()));
            }
        }
    });
});

function delete_product(id) {
    $.ajax({
        url: 'execute/handler/product.php?action=delete&id='+id,
        type: 'GET',
        success: function(data) {
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type);
            load(parseInt($("#page").text()));
        }
    });
}

// For orders
function accept(id) {
    $("#id").val(id);
    $("#accept_order").modal("show");
}

$("#f_accept").on('submit', function(e) {
    e.preventDefault();
    $.ajax({
        url: 'execute/handler/orders.php?action=accept&id='+ $("#id").val(),
        type: 'POST',
        data: $(this).serialize(),
        success: function(data) {
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type).then(function() {
                if (obj.type == "success") {
                    $("#serial").val("");
                    $("#accept_order").modal("hide");
                }
            });
            load(parseInt($("#page").text()));
        }
    });
});

function deny(id) {
    $.ajax({
        url: 'execute/handler/orders.php?action=deny&id='+id,
        type: 'GET',
        success: function(data) {
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type);
            load(parseInt($("#page_ship").text()));
        }
    });
}

function done(id) {
    $.ajax({
        url: 'execute/handler/orders.php?action=done&id='+id,
        type: 'GET',
        success: function(data) {
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type);
            load(parseInt($("#page_done").text()));
        }
    });
}


// For category
$("#add_cate").on("submit", function(e) {
    e.preventDefault();
    $.ajax({
        url: 'execute/handler/category.php?action=add',
        type: 'POST',
        data: $(this).serialize(),
        success: function(data) {
            var obj = JSON.parse(data);
            $("#add_category").modal('hide');
            swal(obj.title, obj.message, obj.type);
            $("#cate").val("");
            load(parseInt($("#page").text()));
        }
    });
});

function category_delete(id) {
    $.ajax({
        url: 'execute/handler/category.php?action=delete&id=' + id,
        type: 'GET',
        success: function(data) {
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type);
            load(parseInt($("#page").text()));
        }
    });
}

function category_edit(id, name) {
    $("#id_cate").val(id);
    $("#name_cate").val(name);
    $("#edit_category").modal("show");
}

$("#edit_cate").on("submit", function(e) {
    e.preventDefault();
    $.ajax({
        url: 'execute/handler/category.php?action=edit&id=' + $("#id_cate").val(),
        type: 'POST',
        data: $(this).serialize(), 
        success: function(data) {
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type);
            load(parseInt($("#page").text()));
            $("#edit_category").modal("hide");
        }
    });
});



// For users
function user_edit(id) {
    $("#edit_title").text("Sửa thông tin cho: " + $("#"+ id).attr("data-username"));
    $("#edit_username").val($("#"+ id).attr("data-username"));
    $("#edit_phone").val($("#"+ id).attr("data-phone"));
    $("#edit_email").val($("#"+ id).attr("data-email"));
    $("#edit_rank").val($("#"+ id).attr("data-rank"));
    
    $("#edit").modal('show');
}

$("#user_edit").on("submit", function(e) {
    e.preventDefault();
    $.ajax({
        url: 'execute/handler/users.php?action=edit',
        type: 'POST',
        data: $(this).serialize(),
        success: function(data) {
            $("#edit").modal('hide');
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type);
            load(parseInt($("#page").text()));
        }
    });
});

function user_delete(id) {
    $.ajax({
        url: 'execute/handler/users.php?action=delete&id=' + id,
        type: 'GET',
        success: function(data) {
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type);
            load(parseInt($("#page").text()));
        }
    });
}




// For settings
$("#basic").submit(function(e) {
    e.preventDefault();    
    var formData = new FormData(this);
    
    $.ajax({
        url: 'execute/handler/settings.php?type=basic',
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            console.log(data);
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type);
            $("#icon").val("");
            $("#logo").val("");
            $("#banner").val("");
        }
    });
});

$("#meta").submit(function(e) {
    e.preventDefault();    
    $.ajax({
        url: 'execute/handler/settings.php?type=meta',
        type: 'POST',
        data: $(this).serialize(),
        success: function (data) {
            console.log(data);
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type);
        }
    });
});

$("#home").submit(function(e) {
    e.preventDefault();    
    $.ajax({
        url: 'execute/handler/settings.php?type=home',
        type: 'POST',
        data: $(this).serialize(),
        success: function (data) {
            console.log(data);
            var obj = JSON.parse(data);
            swal(obj.title, obj.message, obj.type);
        }
    });
});


$("#color").bind('input', function() {
    $("#i_color").val($(this).val());
});

$("#i_color").bind('input', function() {
    $("#color").val($(this).val());
});

$("#title-color").bind('input', function() {
    $("#t-color").val($(this).val());
});

$("#t-color").bind('input', function() {
    $("#title-color").val($(this).val());
});

$("#subtitle-color").bind('input', function() {
    $("#st-color").val($(this).val());
});

$("#st-color").bind('input', function() {
    $("#subtitle-color").val($(this).val());
});

