'use client'
import { ChangeEvent, useActionState, useEffect, useState } from "react";
import { createProduct, editProduct, Product } from "../actions/products";



const formataReais = Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format

function ProductsItem(product: Product) {
  const [isEditing, setEditing] = useState(false)
  const [productState, formAction, pending] = useActionState(editProduct, product)
  const [productChanges, setProductChanges] = useState<Product>(productState)

  function handlEditProduct() {
    formAction(productChanges)
    setEditing(false)
  }

  function handleProductClick() {
    if (!isEditing) {
      setEditing(true)
    }
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
    const { name, value, type } = e.target
    setProductChanges(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value
    }))
  }

  function handleCancel() {
    setEditing(false)
  }

  return <>
    <div className="p-2 flex-1 min-w-0 space-y-2">
      {isEditing ? (
        <form action={handlEditProduct} className="">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nome do Produto
            </label>
            <input
              type="text"
              name="name"
              value={productChanges.name}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-700"
              placeholder="Nome do produto"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Preço</label>
              <input
                type="number"
                name="price_per_quantity"
                value={productChanges.price_per_quantity}
                onChange={handleChange}
                step="0.01"
                min="0"
                className="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-700"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Unidade</label>
              <select
                name="unit_of_measurement"
                value={productChanges.unit_of_measurement}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-700"
              >
                <option value="un">Unidade (un)</option>
                <option value="kg">Quilograma (kg)</option>
                <option value="g">Grama (g)</option>
                <option value="l">Litro (l)</option>
                <option value="ml">Mililitro (ml)</option>
                <option value="cx">Caixa (cx)</option>
                <option value="pct">Pacote (pct)</option>
              </select>
            </div>
          </div>


          <div className="flex flex-wrap gap-2 pt-2">
            <button
              type="submit"
              className="px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors cursor-pointer flex-1"
            >
              Salvar
            </button>
            <button
              type="button"
              className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition-colors cursor-pointer flex-1"
            >
              Excluir
            </button>
            <button
              type="button"
              className="px-3 py-1 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors cursor-pointer w-full"
              onClick={handleCancel}
            >
              Cancelar
            </button>
          </div>
        </form>
      ) : (
        <div className="cursor-pointer bg-white hover:bg-gray-100 p-2 rounded-sm" onClick={handleProductClick}>
          <p className="truncate"><strong>{productState.name || 'Produto sem nome'}</strong></p>
          <p className="truncate"><strong>Preço:</strong> {formataReais(productState.price_per_quantity)} <em>por</em> {productState.unit_of_measurement || 'un.'}</p>
          <p className="truncate"><strong>Quantidade:</strong> {productState.quantity} {productState.unit_of_measurement || 'un.'}</p>
          <p className="truncate"><strong>Total:</strong> {formataReais(productState.price_per_quantity * productState.quantity)}</p>
        </div>
      )}
    </div>
  </>

}


export default function Products(
  initialState: { 
    products: Product[]
    error?: string
    onProductsChange: (products: Product[]) => void
  }
) {
  const [unitOfMeasure, setUnitOfMeasure] = useState('un.')
  const [state, formAction, pending] = useActionState(createProduct, initialState)

  function handleUnitChange(e: ChangeEvent) {
    const target = e.target! as HTMLInputElement
    const value = target.value;
    setUnitOfMeasure(value);
  }

  useEffect(() => {
    if (state?.products) {
      initialState.onProductsChange(state?.products)
    }
  }, [state])

  return <details open={false}>
    <summary className="text-xl cursor-pointer bg-gray-200 p-2">Produtos em estoque</summary>
    <div className="px-4 mt-6">
      <details
        className="border border-gray-300 rounded-sm"
        open={(state?.products || []).length == 0}
      >
        <summary
          className="list-none cursor-pointer  p-2"
        >
          <span className="mdi mdi-plus"></span> 
          Cadastrar produto
        </summary>

        <form
          action={formAction}
          className="flex flex-wrap space-y-2 p-2"
        >
          <p>{state?.error}</p>

          <div className="p-1 w-full">
            <label
              htmlFor="product-name"
              className="block text-sm font-medium text-gray-700 mb-1">
              Nome do produto
            </label>
            <input
              className="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-700"
              type="text"
              id="product-name"
              name="product-name"
              placeholder="Fertilizante"
            />
          </div>

          <div className="p-1 w-full md:w-1/2">
            <label
              htmlFor="product-price"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Preço por {unitOfMeasure}
            </label>
            <input
              className="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-700"
              type="number"
              id="product-price"
              name="product-price"
              step="0.01"
              placeholder="0,00"
            />
          </div>

          <div className="p-1 w-full md:w-1/2">
            <label
              htmlFor="product-unit"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Unidade de medida
            </label>
            <input
              className="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-700"
              type="text"
              id="product-unit"
              name="product-unit"
              value={unitOfMeasure}
              onChange={handleUnitChange}
            />
          </div>

          <button
            className="bg-gray-100 p-2 m-1 w-full cursor-pointer hover:bg-gray-200"
            type="submit"
          >
            Cadastrar
          </button>
        </form>
      </details>

      <div className="overflow-scroll max-h-96 mt-4">
        {state?.products?.length === 0 ? (
          <p className="text-center">Nenhum produto cadastrado</p>
        ) : (
          <ul className="">
            {state?.products?.map((product: Product) => (
              <li
                className="border-b border-gray-300 flex"
                key={product.uuid}
              >
                <ProductsItem {...product} />
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  </details>
}
