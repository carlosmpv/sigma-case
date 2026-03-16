'use client'

import type { Transaction } from "../actions/products"

const formataReais = Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format

export default function Transactions(
  state: {
    transactions: Transaction[],
    total: number
  }
) {
  return <details open={false}>
    <summary className="text-xl cursor-pointer bg-gray-200 p-2">Histórico de transações</summary>
    <div className="px-4 mt-6">
      <div className="border border-gray-300 rounded-sm p-2">Total: {formataReais(state.total ?? 0)}</div>
      <div className="overflow-scroll max-h-96 mt-4">
        {state?.transactions?.length === 0 ? (
          <p className="text-center">Nenhum produto cadastrado</p>
        ) : (
          <ul className="">
            {state?.transactions?.map((transaction: Transaction) => (
              <li
                className="border-b border-gray-300 flex"
                key={transaction.when}
              >
                <div className="p-2 flex-1 min-w-0 space-y-2">
                  <div className="cursor-pointer bg-white hover:bg-gray-100 p-2 rounded-sm">
                    <p className="truncate"><strong>{transaction.updated_product.name || 'Produto sem nome'}</strong></p>
                    <p className="truncate"><strong>Valor:</strong> {formataReais(transaction.updated_product.price_per_quantity)} por {transaction.updated_product.unit_of_measurement || 'un.'}</p>
                    <p className="truncate"><strong>Quantidade:</strong> {transaction.quantity} {transaction.updated_product.unit_of_measurement || 'un.'}</p>
                    <p className="truncate"><strong>Total:</strong> {formataReais(transaction.quantity * transaction.updated_product.price_per_quantity)}</p>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  </details>
}