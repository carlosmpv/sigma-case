'use client'

import { useActionState, useEffect } from "react";
import { signin } from "../actions/auth";
import { useRouter } from "next/navigation";

const initialState = {
  error: '',
  success: false,
}

export default function SigninForm() {
  const [state, formAction, pending] = useActionState(signin, initialState)
  const router = useRouter()
  useEffect(() => {
    if (state.success) {
      router.push('/dashboard')
    }
  }, [state, router]);

  return <>
    <div id="signin" className="bg-gray-50 p-8 rounded-xl">
      <h2 className="text-3xl font-bold mb-6">Entrar</h2>
      <form className="space-y-6" id="signin-form" action={formAction}>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
            E-mail
          </label>
          <input
            type="email"
            id="email"
            name="email"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
            placeholder="seu@email.com"
          />
        </div>
        <div>
          <label htmlFor="senha" className="block text-sm font-medium text-gray-700 mb-2">
            Senha
          </label>
          <input
            type="senha"
            id="senha"
            name="senha"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
            placeholder="••••••••"
          />
        </div>
        <button
          type="submit"
          className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700 cursor-pointer transition font-medium"
        >
          Entrar
        </button>
      </form>
    </div>
  </>
}