let showedCitiesNumber = 10;
function categorySidebarClicked(categorySidebarId, categorySidebarTitle){
    // get the category id for query in ajax

    console.log("---" + categorySidebarId)
    let list = categorySidebarId.split('-');
    let submenuId = `submenu-for-${categorySidebarId}`;
    let iconId = `sidebar-icon-for-${list[list.length-1]}`;
    let isRotated = $(`#${iconId}`).hasClass("rotate-down-category");
    if (!isRotated){
        $(`#${iconId}`).addClass('rotate-down-category');
    } else {
        $(`#${iconId}`).removeClass('rotate-down-category');
    }

    baseSidebar(list[list.length-1], submenuId);

    // $(`#${submenuId}`).toggle(300)

}

function baseCategorySidebarClicked(baseCategorySidebarId, baseCategoryId) {
    let submenuId = `submenu-for-base-category-${baseCategoryId}`;
    let list = baseCategorySidebarId.split('-');
    let iconId = `sidebar-icon-for-base-${list[list.length-1]}`;
    let isRotated = $(`#${iconId}`).hasClass("rotate-down-base-category");
    if (!isRotated){
        $(`#${iconId}`).addClass('rotate-down-base-category');
    } else {
        $(`#${iconId}`).removeClass('rotate-down-base-category');
    }
    console.log(iconId);
    // console.log(submenuId);
    // console.log(baseCategorySidebarId);

    materialCategorySidebar(list[list.length-1], submenuId)
}

function materialCategorySidebarClicked(materialCategorySidebarId, materialCategoryId) {
    let submenuId = `submenu-for-material-category-${materialCategoryId}`;
    let list = materialCategorySidebarId.split('-');
    let iconId = `sidebar-icon-for-material-${list[list.length-1]}`;
    let isRotated = $(`#${iconId}`).hasClass("rotate-down-material-category");
    if (!isRotated){
        $(`#${iconId}`).addClass('rotate-down-material-category');
    } else {
        $(`#${iconId}`).removeClass('rotate-down-material-category');
    }
    console.log(list);
    console.log(submenuId);
    materialSidebar(list[list.length-1], submenuId)
}

function materialSidebarClicked() {

}

function baseSidebar(categoryId, submenuCategoryId){
    if($.trim($(`#${submenuCategoryId}`).html()) === ''){
        $.ajax({
            url: url_base_category,
            type: "GET",
            dataType: 'json',
            data: {
                'c': categoryId
            },
            success: function (data) {
                // console.log(JSON.stringify(data));
                let baseCategoryTitle = [];
                let baseCategoryId = [];
                let categoryId = null;
                data.map(item => {
                    baseCategoryTitle.push(item.title);
                    baseCategoryId.push(item.id);
                    categoryId = (item.category);
                });
                for (let i = 0; i < baseCategoryId.length; i++) {
                    // console.log(baseCategoryId[i]);
                    $(`#${submenuCategoryId}`).append(
                        `<li style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis">` +
                            `<a style="cursor: pointer" onclick="baseCategorySidebarClicked(id, ${baseCategoryId[i]})" id="sidebar-base-category-${baseCategoryId[i]}">` +
                                `<i class="fa fa-chevron-left align-middle ml-2" id="sidebar-icon-for-base-${baseCategoryId[i]}" style="color: gray; font-size: 10px"> </i>` +
                            `</a>` +
                            `<a href="${url_base}" onclick="this.href += '${baseCategoryId[i]}' + '/base-category/'" style="cursor: pointer; font-size: 13px" data-toggle="tooltip" title="${baseCategoryTitle[i]}">${baseCategoryTitle[i]}</a>` +
                            `<ul class="list-unstyled submenu" id="submenu-for-base-category-${baseCategoryId[i]}" style="margin-right: -20px"> </ul>` +
                        `</li>`
                    );
                }
                $(`#${submenuCategoryId}`).toggle(350)
            }
        });
    } else {
        $(`#${submenuCategoryId}`).toggle(300);
    }

    // console.log("yes")
}

function materialCategorySidebar(baseCategoryId, submenuBaseCategoryId){

    if($.trim($(`#${submenuBaseCategoryId}`).html()) === ''){
        $.ajax({
            url: url_material_category,
            type: "GET",
            dataType: 'json',
            data: {
                'c': baseCategoryId
            },
            success: function (data) {
                // console.log(JSON.stringify(data));
                let materialCategoryTitle = [];
                let materialCategoryId = [];
                let baseCategoryId = null;
                data.map(item => {
                    materialCategoryTitle.push(item.title);
                    materialCategoryId.push(item.id);
                    baseCategoryId = (item.category);
                });
                for (let i = 0; i < materialCategoryId.length; i++) {
                    // console.log(baseCategoryId[i]);
                    $(`#${submenuBaseCategoryId}`).append(
                        `<li style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis">` +
                            `<a style="cursor: pointer" onclick="materialCategorySidebarClicked(id, ${materialCategoryId[i]})" id="sidebar-material-category-${materialCategoryId[i]}">` +
                                `<i class="fa fa-chevron-left align-middle ml-2" id="sidebar-icon-for-material-${materialCategoryId[i]}" style="color: gray; font-size: 10px"> </i>` +
                            `</a>` +
                            `<a href="${url_base}" onclick="this.href += '${materialCategoryId[i]}' + '/material-category/'" style="cursor: pointer; font-size: 13px" data-toggle="tooltip" title="${materialCategoryTitle[i]}">${materialCategoryTitle[i]}</a>` +
                            `<ul class="list-unstyled submenu" id="submenu-for-material-category-${materialCategoryId[i]}" style="margin-right: -20px"> </ul>` +
                        `</li>`
                    );
                }
                $(`#${submenuBaseCategoryId}`).toggle(350)
            }
        })
    } else {
        $(`#${submenuBaseCategoryId}`).toggle(350)
    }
}

function materialSidebar(materialCategoryId, submenuMaterialCategoryId){

    if($.trim($(`#${submenuMaterialCategoryId}`).html()) === ''){
        $.ajax({
            url: url_material,
            type: "GET",
            dataType: 'json',
            data: {
                'c': materialCategoryId
            },
            success: function (data) {
                console.log(JSON.stringify(data));
                let materialTitle = [];
                let materialId = [];
                let materialCategoryId = null;
                data.map(item => {
                    materialTitle.push(item.title);
                    materialId.push(item.id);
                    materialCategoryId = (item.category);
                });
                for (let i = 0; i < materialId.length; i++) {
                    // console.log(baseCategoryId[i]);
                    $(`#${submenuMaterialCategoryId}`).append(
                        `<li style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis">` +
                            `<a style="cursor: pointer" onclick="materialSidebarClicked(id, ${materialId[i]})" id="sidebar-material-${materialCategoryId[i]}"><i class="fa fa-chevron-left align-middle ml-2" style="color: gray; font-size: 10px"> </i></a>` +
                            `<a href="${url_base}" onclick="this.href += '${materialId[i]}' + '/material/products'" style="cursor: pointer; font-size: 13px;" data-toggle="tooltip" title="${materialTitle[i]}">${materialTitle[i]}</a>` +
                            `<ul class="list-unstyled submenu" id="submenu-for-material-${materialId[i]}" style="margin-right: -20px"> </ul>` +
                        `</li>`
                    );
                }
                $(`#${submenuMaterialCategoryId}`).toggle(350)
            }
        })
    } else {
        $(`#${submenuMaterialCategoryId}`).toggle(350)
    }
}

filteringCities();


function filteringCities() {
    let citiesFilter = [];
    let holder = $(".checkbox-input");
    let holderLabel = $(".my-checkbox");

    for(let i = 0; i < holder.length; i++){
        let itm = holder.eq(i);
        if (itm.prop('checked') === true) {
            citiesFilter.push(itm.attr('value'));
        }
    }

    //-- show/hide cities --//

    for(let i = 0; i < holder.length && i < showedCitiesNumber; i++){
        let itm = holder.eq(i);
        let itm_lbl = holderLabel.eq(i);
        itm.show();
        itm_lbl.show();
    }
    for(let i = showedCitiesNumber; i < holder.length ; i++){
        let itm = holder.eq(i);
        let itm_lbl = holderLabel.eq(i);
        itm.hide();
        itm_lbl.hide();
    }

    let citiesStr = citiesFilter.join(',');
    return citiesStr;
}

$("#filtering-done-btn").click(function () {
    let whereWeAre = $("#where-we-are").attr('current-url');
    console.log(whereWeAre);
    let product_companies_url = $("#product-companies-url").attr('data-url');
    let electronic_products_url = $("#electronic-products-url").attr('data-url');
    let mechanic_products_url = $("#mechanic-products-url").attr('data-url');
    let structure_products_url = $("#structure-products-url").attr('data-url');
    let electronic_companies_url = $("#electronic-companies-url").attr('data-url');
    let mechanic_companies_url = $("#mechanic-companies-url").attr('data-url');
    let structure_companies_url = $("#structure-companies-url").attr('data-url');
    let advance_search_url = $("#advance-search-url").attr('data-url');
    let search_url = $("#search-url").attr('data-url');
    let search_products_url = $("#search-products-url").attr('data-url');

    // $("#elec-companies-search-btn").click();
    if(whereWeAre.indexOf(product_companies_url) > -1){
        // $("#advance-search-submit").click()
    }
    else if(whereWeAre.indexOf(electronic_products_url) > -1){
        $("#elec-products-search-btn").click();
    }
    else if(whereWeAre.indexOf(mechanic_products_url) > -1){
        $("#mech-products-search-btn").click();
    }
    else if(whereWeAre.indexOf(structure_products_url) > -1){
        $("#struct-products-search-btn").click();
    }
    else if(whereWeAre.indexOf(electronic_companies_url) > -1){
        $("#elec-companies-search-btn").click();
    }
    else if(whereWeAre.indexOf(mechanic_companies_url) > -1){
        $("#mech-companies-search-btn").click();
    }
    else if(whereWeAre.indexOf(structure_companies_url) > -1){
        $("#struct-companies-search-btn").click();
    }
    else if(whereWeAre.indexOf(advance_search_url) > -1){
        $("#advance-search-submit").click()
    }
    else if(whereWeAre.indexOf(search_url) > -1){
        filter_search_cities();
    }
    else if(whereWeAre.indexOf(search_products_url) > -1){
        applyCitiesFilterInSearchProduct();
    }
});

$('#city-filtering-more-btn').click(function () {
    let status = $('#city-filtering-more-btn').attr('value');
    if(status === "unexpanded"){
        $('#city-filtering-more-btn').attr('value', 'expanded');
        $('#city-filtering-more-btn').empty();
        $('#city-filtering-more-btn').append(
            `بستن` +
            `<i class="fa fa-chevron-up align-middle mr-1" style="font-size: 10px"></i>`
        );
        showedCitiesNumber = 100;
    }
    else {
        $('#city-filtering-more-btn').attr('value', 'unexpanded');
        $('#city-filtering-more-btn').empty();
        $('#city-filtering-more-btn').append(
            `بیشتر` +
            `<i class="fa fa-chevron-left align-middle mr-1" style="font-size: 10px"></i>`

        );
        showedCitiesNumber = 10;
    }

    let holder = $(".checkbox-input");
    let holderLabel = $(".my-checkbox");

    // console.log(holder.length);

    for(let i = 0; i < holder.length && i<showedCitiesNumber; i++){
       let itm = holder.eq(i);
       let itm_lbl = holderLabel.eq(i);
       itm.show(50);
       itm_lbl.show(50);
   }
    for(let i = showedCitiesNumber; i < holder.length ; i++){

        let itm = holder.eq(i);
        let itm_lbl = holderLabel.eq(i);
        itm.hide(50);
        itm_lbl.hide(50);
    }

});


$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
});