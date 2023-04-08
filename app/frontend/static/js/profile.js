// const products = [
//     {
//       id: 0,
//       product_name: "T-Shirt",
//       price: "20.99",
//       image: "https://zajo.bwcdn.net/media/2022/08/1/8/sk-litio-t-shirt-ss-18105-size-large-v-2.webp",
//       wedsite_base_url: "https://www.emag.ro/laptop-hp-250-g9-cu-procesor-intelr-coretm-i5-1235u-pana-la-4-40-ghz-15-6-full-hd-8gb-256gb-ssd-intelr-irisr-xe-graphics-free-dos-dark-ash-silver-6f1z9ea/pd/DJ2VBZMBM/"
//     },
//     {
//       id: 1,
//       product_name: "Jeans",
//       price: "20.99",
//       image: "https://cdn.aboutstatic.com/file/images/bcb57d5438e332206b0edbaaabbb7719.jpg?brightness=0.96&quality=75&trim=1&height=1280&width=960",
//       wedsite_base_url: "https://www.emag.ro/laptop-hp-250-g9-cu-procesor-intelr-coretm-i5-1235u-pana-la-4-40-ghz-15-6-full-hd-8gb-256gb-ssd-intelr-irisr-xe-graphics-free-dos-dark-ash-silver-6f1z9ea/pd/DJ2VBZMBM/"
//     },
//     {
//       id: 2,
//       product_name: "Hoodie",
//       price: "29.99",
//       image: "https://cermariner.ro/wp-content/uploads/2019/05/hoodie-with-zipper.jpg",
//       wedsite_base_url: "https://www.emag.ro/laptop-hp-250-g9-cu-procesor-intelr-coretm-i5-1235u-pana-la-4-40-ghz-15-6-full-hd-8gb-256gb-ssd-intelr-irisr-xe-graphics-free-dos-dark-ash-silver-6f1z9ea/pd/DJ2VBZMBM/"
//     }
//     ,
//     {
//       id: 3,
//       product_name: "Laptop",
//       price: "4000.00",
//       image: "https://s13emagst.akamaized.net/products/48965/48964051/images/res_2068b30b9c607880faaa2f433bb28b42.jpg?width=450&height=450&hash=1FE0D22EE07A6F995A904FA11386132E",
//       wedsite_base_url: "https://www.emag.ro/laptop-hp-250-g9-cu-procesor-intelr-coretm-i5-1235u-pana-la-4-40-ghz-15-6-full-hd-8gb-256gb-ssd-intelr-irisr-xe-graphics-free-dos-dark-ash-silver-6f1z9ea/pd/DJ2VBZMBM/"
//     }
// ];

async function getProducts(){
      const username1 = "robert@test.com";
      const token1 = "generatedByFastapi";
      var sites1 = [];
      const siteElements = document.getElementsByName('checkbox');
      for(var siteElement of siteElements){
        if(siteElement.checked){
             sites1.push(siteElement.value);
        }
      }
      const order1 = document.querySelector('input[name="option"]:checked').value;
      const jsonBody = {
        username: username1,
        sites: sites1,
        order: order1,
        token: token1
      };
      const response = await fetch('/get_cart', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonBody),
      });
      const response_json = await response.json();
      ex(response_json.products);
  }

function ex(products) {
    for (let i = 0; i < products.length; i++) {
      const product = products[i];
      let cards_boots=`
              <div class="card col-12">
              <div class="row">
              <div class="crop col-12" style="width:100%">
                   <img src=${product.image} alt="Card image cap">
              </div>
              <div class="card-body col-12">
                  <h5 class="card-title">${product.product_name}</h5>
                  <a href="${product.website_base_url}" class="btn btn-primary">${product.price}</a>
              </div>
              </div>
              </div>
              `;
              document.getElementById("product-list-tag-id").innerHTML +=cards_boots;
    }
}
