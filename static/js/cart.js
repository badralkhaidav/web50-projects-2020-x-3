var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){

		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if(document.getElementById(productId)==undefined){var topping_description=""}
		else{
		var x = document.getElementById(productId);
		var topping_description = Array.from(x.selectedOptions).map(option => option.value)
		}

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action, topping_description)
		}else{
			updateUserOrder(productId, action, topping_description)
		}
	})
}

	function topping_change(productId, toppingnumber, action,value){

		var x = document.getElementById(productId);
		var topping_description = Array.from(x.selectedOptions).map(option => option.value)

			if(toppingnumber > topping_description.length){

				cart[productId]= {'topping_description': topping_description}

				for(i=0; i< x.length;i++){
					if(x[i].selected){
						x[i].disabled = false
					}
					else {
						x[i].disabled = false
					}
				}
			}

			if(toppingnumber == topping_description.length){

				for(i=0; i< x.length;i++){
					if(x[i].selected){
						x[i].disabled = false
					}
					else {
						x[i].disabled = true
					}
				}
				console.log("Limit rich")

			}

			if(toppingnumber < topping_description.length){
				//last selected-iig unselect hiih heregtei
				alert("Topping number:", toppingnumber)
				topping_reduce = x.length
				for(i=0; i< x.length;i++){
					if(x[i].selected){
						x[i].disabled = false
						if(topping_reduce>toppingnumber){
							topping_reduce=topping_reduce-1
							x[i].selected=false
						}
					}
					else {
						x[i].disabled = true
					}
				}
				console.log("Limit rich")

			}

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action, topping_description)
		}else{
			updateUserOrder(productId, action, topping_description)
		}

		location.reload();
	}

function updateUserOrder(productId, action, topping_description){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'productId':productId, 'action':action, 'topping_description': topping_description})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(productId, action, topping_description){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}
		else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	if (action == 'select_topping'){
		cart[productId]['topping_description']= topping_description
		console.log('Select option')
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

	//location.reload()
}
