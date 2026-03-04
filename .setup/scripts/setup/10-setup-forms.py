#!/usr/bin/env python3

# What this script does:
# - Installs react-hook-form, zod, and @hookform/resolvers (if not already present)
# - Creates src/app/forms-page.tsx — a signup-style form demonstrating:
#   - Text input with min-length validation (name)
#   - Email input with format validation (email)
#   - Number input with optional range validation (age)
#   - Select with required validation (role)
#   - Textarea with max-length validation (bio)
#   - Checkbox with required acceptance (terms)
#   - Success panel displaying submitted values
# - Patches src/routing/router.tsx to add the /forms route
# - Patches src/app/app.tsx nav to add a Forms link
# - Runs eslint --fix on all new and modified files

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run(cmd: str, allow_nonzero: bool = False) -> None:
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode != 0 and not allow_nonzero:
        raise SystemExit(f"Command failed: {cmd}")


# ---------------------------------------------------------------------------
# File contents
# ---------------------------------------------------------------------------

FORMS_PAGE_TSX = """\
import { useState } from 'react';
import { useForm } from 'react-hook-form';

import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

import { Button } from '../controls/button';
import { Checkbox } from '../controls/checkbox';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '../controls/form';
import { Input } from '../controls/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../controls/select';
import { Textarea } from '../controls/textarea';

const formSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  age: z
    .string()
    .refine(
      (val) =>
        val === '' ||
        (!isNaN(Number(val)) && Number(val) >= 18 && Number(val) <= 120),
      { message: 'Age must be a number between 18 and 120' },
    )
    .optional(),
  role: z.string().min(1, 'Please select a role'),
  bio: z.string().max(200, 'Bio must be at most 200 characters').optional(),
  acceptTerms: z
    .boolean()
    .refine((val) => val === true, {
      message: 'You must accept the terms and conditions',
    }),
});

type FormValues = z.infer<typeof formSchema>;

export function FormsPage() {
  const [submitted, setSubmitted] = useState<FormValues | null>(null);

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: '',
      age: '',
      role: '',
      bio: '',
      acceptTerms: false,
    },
  });

  function onSubmit(values: FormValues): void {
    setSubmitted(values);
    form.reset();
  }

  return (
    <div className='space-y-8'>
      <div>
        <h1 className='text-2xl font-bold'>Forms &amp; Validation</h1>
        <p className='mt-1 text-sm text-muted-foreground'>
          Demonstrates react-hook-form with Zod validation using shadcn/ui form
          components.
        </p>
      </div>

      <Form {...form}>
        <form
          className='max-w-md space-y-6'
          onSubmit={form.handleSubmit(onSubmit)}
        >
          <FormField
            control={form.control}
            name='name'
            render={({ field }) => (
              <FormItem>
                <FormLabel>Full Name</FormLabel>
                <FormControl>
                  <Input placeholder='Jane Doe' {...field} />
                </FormControl>
                <FormDescription>Your full display name.</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name='email'
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input
                    placeholder='jane@example.com'
                    type='email'
                    {...field}
                  />
                </FormControl>
                <FormDescription>
                  We will never share your email.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name='age'
            render={({ field }) => (
              <FormItem>
                <FormLabel>Age (optional)</FormLabel>
                <FormControl>
                  <Input
                    className='w-32'
                    max={120}
                    min={18}
                    placeholder='25'
                    type='number'
                    {...field}
                  />
                </FormControl>
                <FormDescription>Must be 18 or older.</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name='role'
            render={({ field }) => (
              <FormItem>
                <FormLabel>Role</FormLabel>
                <Select value={field.value} onValueChange={field.onChange}>
                  <FormControl>
                    <SelectTrigger className='w-48'>
                      <SelectValue placeholder='Select a role' />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value='admin'>Admin</SelectItem>
                    <SelectItem value='editor'>Editor</SelectItem>
                    <SelectItem value='viewer'>Viewer</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name='bio'
            render={({ field }) => (
              <FormItem>
                <FormLabel>Bio (optional)</FormLabel>
                <FormControl>
                  <Textarea
                    className='min-h-24 resize-none'
                    placeholder='Tell us a little about yourself.'
                    {...field}
                  />
                </FormControl>
                <FormDescription>Max 200 characters.</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name='acceptTerms'
            render={({ field }) => (
              <FormItem className='flex flex-row items-start space-x-3 space-y-0'>
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                </FormControl>
                <div className='space-y-1 leading-none'>
                  <FormLabel>Accept terms and conditions</FormLabel>
                  <FormDescription>
                    You agree to our terms of service and privacy policy.
                  </FormDescription>
                  <FormMessage />
                </div>
              </FormItem>
            )}
          />

          <Button type='submit'>Submit</Button>
        </form>
      </Form>

      {submitted !== null && (
        <div className='max-w-md rounded-lg border border-green-200 bg-green-50 p-4'>
          <h2 className='mb-2 font-semibold text-green-800'>
            Form submitted successfully!
          </h2>
          <pre className='text-sm text-green-700'>
            {JSON.stringify(submitted, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def ensure_installed() -> None:
    """Install react-hook-form, zod, @hookform/resolvers if missing."""
    pkg_json = (ROOT / "package.json").read_text()
    missing = [
        p
        for p in ("react-hook-form", "zod", "@hookform/resolvers")
        if p not in pkg_json
    ]
    if missing:
        pkgs = " ".join(missing)
        run(f"bun add {pkgs}")
    else:
        print("  already installed  react-hook-form zod @hookform/resolvers")


def create_forms_page() -> None:
    dest = ROOT / "src" / "app" / "forms-page.tsx"
    dest.write_text(FORMS_PAGE_TSX)
    print("  created  src/app/forms-page.tsx")


def patch_router() -> None:
    path = ROOT / "src" / "routing" / "router.tsx"
    src = path.read_text()

    if "FormsPage" in src:
        print("  skipped  src/routing/router.tsx (already patched)")
        return

    # Add import after the last app import line
    src = src.replace(
        "import { TailwindPage } from '../app/tailwind-page';",
        "import { FormsPage } from '../app/forms-page';\nimport { TailwindPage } from '../app/tailwind-page';",
    )

    # Add route after controls route
    src = src.replace(
        "{ path: 'controls', element: <ControlsPage /> },",
        "{ path: 'controls', element: <ControlsPage /> },\n      { path: 'forms', element: <FormsPage /> },",
    )

    path.write_text(src)
    print("  patched  src/routing/router.tsx")


def patch_app() -> None:
    path = ROOT / "src" / "app" / "app.tsx"
    src = path.read_text()

    if "to='/forms'" in src:
        print("  skipped  src/app/app.tsx (already patched)")
        return

    src = src.replace(
        "<Link style={linkStyle} to='/controls'>\n          Controls\n        </Link>",
        "<Link style={linkStyle} to='/controls'>\n          Controls\n        </Link>\n        <Link style={linkStyle} to='/forms'>\n          Forms\n        </Link>",
    )

    path.write_text(src)
    print("  patched  src/app/app.tsx")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print(f"Root: {ROOT}\n")

    print("[1] Ensure react-hook-form, zod, @hookform/resolvers are installed")
    ensure_installed()

    print("\n[2] Create src/app/forms-page.tsx")
    create_forms_page()

    print("\n[3] Patch src/routing/router.tsx")
    patch_router()

    print("\n[4] Patch src/app/app.tsx")
    patch_app()

    print("\n[5] Fix import ordering and linting")
    run(
        "bunx eslint --fix src/app/forms-page.tsx src/routing/router.tsx src/app/app.tsx"
    )

    print("\nDone.")


if __name__ == "__main__":
    main()
