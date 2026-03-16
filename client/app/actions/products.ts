'use server'

import { getAccessToken } from "@/utils/token";


export type Product = {
  uuid: string
  name: string
  price_per_quantity: number
  quantity: number
  unit_of_measurement: string
};

export type ProductUpdatePayload = {
  uuid: string
  name?: string
  price_per_quantity?: number
  quantity?: number
  unit_of_measurement?: string
}

export async function getProducts(): Promise<Product[]> {
  const token = await getAccessToken()!

  const response = await fetch(`${process.env.API_URL}/secured/products`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  const procuts = await response.json() as Product[];
  return procuts.reverse() // Reverte para que os novos fiquem no topo
}

export async function createProduct(prevState: any, payload: FormData) {
  const token = await getAccessToken()!

  const response = await fetch(`${process.env.API_URL}/secured/products`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "name": payload.get('product-name')! as string,
      "price_per_quantity": Number(payload.get('product-price')!),
      "quantity": Number(payload.get('product-quantity')!),
      "unit_of_measurement": payload.get('product-unit')! as string,
    })
  })

  if (!response.ok) {
    const { detail } = await response.json()
    return {
      ...prevState,
      error: detail || "Erro ao criar produto"
    }
  }

  const newProduct = await response.json() as Product
  return {
    products: [newProduct, ...(prevState?.products as Product[])],
    error: '',
  }
}

export async function editProduct(prevState: any, payload: ProductUpdatePayload) {
  const token = await getAccessToken()!
  
  const response = await fetch(`${process.env.API_URL}/secured/products/${payload.uuid}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })

  if (!response.ok) {
    return prevState
  }

  return {...prevState, ...payload}
}

export async function deleteProduct(prevState: any, targetID: string) {
  const token = await getAccessToken()!

  const response = await fetch(`${process.env.API_URL}/secured/products/${targetID}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
}

export type Transaction = {
  updated_product: Product
  when: string
  quantity: number
  lat: number
  lng: number
}

export async function transactionHistory() {
  const token = await getAccessToken()!

  const response = await fetch(`${process.env.API_URL}/secured/transaction/history`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  return await response.json() as Transaction[]
}

export async function buyProduct(productID: string, payload: {quantity: number, lng: number, lat: number}) {
  const token = await getAccessToken()!
  
  const response = await fetch(`${process.env.API_URL}/secured/transaction/buy/${productID}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })

  return await response.json() as Transaction
}

export async function sellProduct(productID: string, payload: {quantity: number, lng: number, lat: number}) {
  const token = await getAccessToken()!
  
  const response = await fetch(`${process.env.API_URL}/secured/transaction/sell/${productID}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })

  return await response.json() as Transaction
}

export async function regTransaction(prevState: any, formData: FormData) {
  const lat = Number(formData.get('lat')!)
  const lng = Number(formData.get('lng')!)
  const productID = formData.get('product')! as string
  const quantity = Number(formData.get('quantity')!)
  const transactionType = formData.get('transactionType')! as string
  

  const transaction = (transactionType == 'buy')
    ? await buyProduct(productID, {
      quantity: quantity,
      lng: lng,
      lat: lat,
    })
    : await sellProduct(productID, {
      quantity: quantity,
      lng: lng,
      lat: lat,
    })

  return [transaction, ...prevState]
}

export async function getTotal() {
  const token = await getAccessToken()!
  
  const response = await fetch(`${process.env.API_URL}/secured/transaction/total`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  return await response.json()
}