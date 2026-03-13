'use client'

import { signup } from "@/app/actions/auth";
import { useActionState, useEffect } from "react";
import { useRouter } from "next/navigation";

const initialState = {
  error: '',
  success: false,
}

export default function SignupForm() {
  const [state, formAction, pending] = useActionState(signup, initialState)
  const router = useRouter()
  useEffect(() => {
    if (state.success) {
      router.push('/dashboard')
    }
  }, [state, router]);

  return <>
    <div id="cadastro" className="bg-gray-50 p-8 rounded-xl">
      <h2 className="text-3xl font-bold mb-2">Cadastro</h2>
      <p className="text-red-700 text-sm font-bold mb-6">{state.error}</p>
      <form className="space-y-6" id="signup-form" action={formAction}>
        <div>
          <label htmlFor="nome" className="block text-sm font-medium text-gray-700 mb-2">
            Nome Completo
          </label>
          <input
            type="text"
            id="nome"
            name="nome"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
            placeholder="João Silva"
          />
        </div>
        <div>
          <label htmlFor="email-cadastro" className="block text-sm font-medium text-gray-700 mb-2">
            E-mail
          </label>
          <input
            type="email"
            id="email-cadastro"
            name="email"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
            placeholder="seu@email.com"
            required={true}
          />
        </div>
        <div>
          <label htmlFor="telefone" className="block text-sm font-medium text-gray-700 mb-2">
            Telefone
          </label>
          <input
            type="tel"
            id="telefone"
            name="telefone"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
            placeholder="(11) 99999-9999"
          />
        </div>
        <div>
          <label htmlFor="data-nascimento" className="block text-sm font-medium text-gray-700 mb-2">
            Data de Nascimento
          </label>
          <input
            type="date"
            id="data-nascimento"
            name="dataNascimento"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
          />
        </div>
        <div>
          <label htmlFor="senha-cadastro" className="block text-sm font-medium text-gray-700 mb-2">
            Senha
          </label>
          <input
            type="password"
            id="senha-cadastro"
            name="senha"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
            required={true}
          />
        </div>
        <div>
          <label htmlFor="confirmar-senha" className="block text-sm font-medium text-gray-700 mb-2">
            Confirmar Senha
          </label>
          <input
            type="password"
            id="confirmar-senha"
            name="confirmarSenha"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
            required={true}
          />
        </div>
        <button
          type="submit"
          className="w-full bg-gray-800 text-white py-3 px-6 rounded-lg hover:bg-gray-900 transition font-medium cursor-pointer"
        >
          Criar Conta
        </button>
      </form>
    </div>
  </>;
}