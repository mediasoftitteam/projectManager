new WOW().init();
new SmoothScroll('a[href*="#"]'),
    {
    easing:'linear',
    speed:1000
};

// add name to breadcrumb
//-- used hidden input in base.html to access django url --//
//-- pagination parameters --//
let nextPage = null;
let currentPage = 1;
let itemCount = -1;     //-- total count of item in the database --//
let itemPerPage = 8;   //-- fetched item count in each try --//
let loading = $("#main-page-loading");

console.log("Main Page");
loading.addClass('loading');
$(window).on('scroll load' , function () {
    //console.log("h = " + $(window).scrollTop());
    if  ($(window).scrollTop()>300){

        $('#go-to-top').css('opacity','1').css('visibility' ,'visible');
    }else
        {
        $('#go-to-top').css('opacity','0').css('visibility' ,'hidden');
    }
});

function showProducts(categoryId){
    $("#main-page-product-loading").addClass('loading');
    // if(itemCount !== -1 && (currentPage - 1) * itemPerPage > itemCount){
    //     console.log("ended");
    //     alert("ended");
    //     $("#all-products-show-more").attr('disabled', 'true');
    //     return
    // }
    loading.addClass('loading');
    $.ajax({
        url: (nextPage === null && currentPage === 1) ? url_company_product : nextPage,
        type: "GET",
        data: {
            'title': "",
            'category': categoryId,
            'page_size': itemPerPage,
        },
        dataType: 'json',
        success: function (data) {
            // console.log(JSON.stringify(data));
            let companyName = [];
            let productTitle = [];
            let companyLocation = [];
            let companyTag = [];
            let productImages = [];
            let productView = $(`#home-${categoryId}-products`);
            let result = data["results"];
            nextPage = data["next"];
            itemCount = data["count"];
            currentPage = currentPage + 1;
            result.map(item => {
                companyName.push(item["company"].title);
                companyLocation.push(item["company"].city);
                companyTag.push(item.category.title);
                productImages.push(item.pictures);
                if(item["subSubMaterial"] !== null){
                    productTitle.push(item["subSubMaterial"].title)
                }
                else if(item["subMaterial"] !== null){
                    productTitle.push(item["subMaterial"].title)
                }
                else if(item["material"] !== null){
                    productTitle.push(item["material"].title)
                }
                else if(item["materialCategory"] !== null){
                    productTitle.push(item["materialCategory"].title)
                }
                else if(item["baseCategory"] !== null){
                    productTitle.push(item["baseCategory"].title)
                }
                else if(item.category !== null){
                    productTitle.push(item.category.title)
                }
                else {
                    productTitle.push("-")
                }


            });
            for(let i = 0; i < productTitle.length; i++){
                let img = JSON.parse(productImages[i]);
                let productPicUrl = "";

                if(img.length > 0){
                    productPicUrl = url_base + "media/" + img[0].pic;
                }
                else if(companyTag[i] === "ابنیه"){
                    productPicUrl = "/static/kootwall/images/MaterialProductIcon.png";
                }
                else if(companyTag[i] === "مکانیک"){
                    productPicUrl = "/static/kootwall/images/MechanicProductIcon.png";
                }
                else if(companyTag[i] === "برق"){
                    productPicUrl = "/static/kootwall/images/ElectricProductIcon.png";
                }
                productView.append(
                    `<div class="col-width" style="direction: ltr ; padding: 5px">` +
                        `<div class="card mb-2" style="width: 100%">` +
                            `<div class="media" style="margin: 5px; background-color: #f7f7f7">` +
                                `<a href="${url_home}" onclick="this.href += ${result[i]["id"]} + '/product/'">` +
                                    `<img src=${productPicUrl} style="width: 120px ; height: 105px" class="align-self-end"  alt="Responsive">` +
                                `</a>` +
                                `<div class="media-body">` +
                                    `<span class="pr-1  d-block" style="color: #307e88 ; font-size: 14px ; padding-top: 5px" id="product-title">` +
                                        ` ${productTitle[i]} ` +
                                    `</span>` +
                                     `<b class="pr-1 mt-2 d-block" style="color: #336799 ; font-size: 14px ; padding-top: 5px" id="product-title">` +
                                        ` ${companyLocation[i]} ` +
                                        `<i class="fa fa-map-marker-alt align-middle ml-1"> </i>` +
                                    `</b>` +
                                `</div>` +
                            `</div>` +
                            `<div class="card-footer"  style="font-size: 12px; padding: 6px;color: #307e88;direction: rtl ">` +
                                `<a href="${url_home}" onclick="this.href += ${result[i]["company"]["id"]} + '/company/'" id="company-name">` +
                                    ` ${companyName[i]} ` +
                                `</a>` +
                            `</div>` +
                        `</div>` +
                    `</div>`
                );
            }
            $("#main-page-product-loading").removeClass('loading');
        },
    })
}

// $('#search-button').click(function (event) {
//     event.preventDefault();
//     nextPage = null;
//     currentPage = 1;
//     itemCount = -1;
//     $("#product-view").empty();
//     showMore();
// });



// $("#show-more-all-products").click(function () {
//     showProducts()
// });

// $(window).scroll(function(){
//     if (Math.floor($(window).scrollTop()) >= $(document).height() - $(window).height() - 5 && Math.floor($(window).scrollTop()) <= $(document).height() - $(window).height() + 5){
//         showMore()
//     }
// });

