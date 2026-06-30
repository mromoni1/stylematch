"use client";

import { signIn } from "next-auth/react";

export default function LandingPage() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-8 text-center">
      <h1 className="text-4xl font-bold tracking-tight">StyleMatch</h1>
      <p className="mt-4 max-w-md text-gray-500">
        Turn your Pinterest boards into a curated secondhand wardrobe. StyleMatch
        reads your saved pins, extracts your aesthetic, and surfaces matching
        listings on Vinted — scored by how well they fit your style.
      </p>
      <button
        onClick={() => signIn("google")}
        className="mt-8 px-6 py-3 rounded-lg bg-black text-white font-medium hover:bg-gray-800 transition-colors"
      >
        Sign in with Google
      </button>
    </main>
  );
}
