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
  return procuts
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
      "unit_of_measure": payload.get('product-unit')! as string,
    })
  })

  if (!response.ok) {
    const { detail } = await response.json()
    console.log('detail', detail)
    return {
      ...prevState,
      error: detail || "Erro ao criar produto"
    }
  }

  const newProduct = await response.json() as Product
  return {
    products: [...(prevState?.products as Product[]), newProduct],
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