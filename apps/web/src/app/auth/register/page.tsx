"use client";

import { useState } from "react";
import { Button, Input } from "@nexus/ui-system";
import { Mail, Lock, User, ArrowRight, Sparkles } from "lucide-react";
import Link from "next/link";
import { motion } from "framer-motion";

export default function RegisterPage() {
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // TODO: implement register
    setTimeout(() => setIsLoading(false), 1000);
  };

  return (
    <div className="flex min-h-screen">
      <div className="flex flex-1 items-center justify-center px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="w-full max-w-sm"
        >
          <div className="mb-8 text-center">
            <div className="mb-4 flex justify-center">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-accent">
                <Sparkles className="h-6 w-6 text-white" />
              </div>
            </div>
            <h1 className="text-2xl font-bold">Create your account</h1>
            <p className="mt-1 text-sm text-text-secondary">
              Start your AI-powered productivity journey
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Full Name"
              placeholder="John Doe"
              leftIcon={<User className="h-4 w-4" />}
              required
            />
            <Input
              label="Email"
              type="email"
              placeholder="you@example.com"
              leftIcon={<Mail className="h-4 w-4" />}
              required
            />
            <Input
              label="Password"
              type="password"
              placeholder="At least 8 characters"
              leftIcon={<Lock className="h-4 w-4" />}
              required
            />
            <Button type="submit" fullWidth isLoading={isLoading}>
              Create Account
              <ArrowRight className="h-4 w-4" />
            </Button>
          </form>

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-primary px-2 text-text-secondary">
                Or continue with
              </span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <Button variant="secondary" fullWidth>
              Google
            </Button>
            <Button variant="secondary" fullWidth>
              GitHub
            </Button>
          </div>

          <p className="mt-6 text-center text-sm text-text-secondary">
            Already have an account?{" "}
            <Link
              href="/auth/login"
              className="font-medium text-accent hover:underline"
            >
              Sign in
            </Link>
          </p>

          <p className="mt-4 text-center text-xs text-text-tertiary">
            By creating an account, you agree to our{" "}
            <Link href="#" className="underline hover:text-text-secondary">
              Terms
            </Link>{" "}
            and{" "}
            <Link href="#" className="underline hover:text-text-secondary">
              Privacy Policy
            </Link>
          </p>
        </motion.div>
      </div>

      <div className="hidden flex-1 bg-gradient-to-br from-accent/10 to-accent-secondary/10 lg:flex lg:items-center lg:justify-center">
        <div className="max-w-md p-12 text-center">
          <h2 className="text-3xl font-bold tracking-tight">
            Your AI Workspace Awaits
          </h2>
          <p className="mt-4 text-text-secondary">
            Chat, manage tasks, track finances, analyze trades, and automate
            workflows — all in one place.
          </p>
        </div>
      </div>
    </div>
  );
}
