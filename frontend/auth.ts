import NextAuth from "next-auth";
import Google from "next-auth/providers/google";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [Google],
  callbacks: {
    jwt({ token, profile }) {
      if (profile) token.google_id = profile.sub;
      return token;
    },
    session({ session, token }) {
      session.user.google_id = token.google_id as string;
      return session;
    },
    async redirect({ url, baseUrl }) {
      if (url === baseUrl || url === `${baseUrl}/`) return `${baseUrl}/setup`;
      return url.startsWith(baseUrl) ? url : baseUrl;
    },
  },
  events: {
    async signIn({ user, account }) {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/users`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          google_id: account?.providerAccountId,
          email: user.email,
        }),
      }).catch(() => {});
    },
  },
});
