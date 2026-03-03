#!/usr/bin/env python3
"""Step 07 – Redux Toolkit setup.

- Installs @reduxjs/toolkit and react-redux.
- Creates src/store/ with:
    store.ts        – configureStore, RootState, AppDispatch
    hooks.ts        – typed useAppDispatch / useAppSelector
    index.ts        – re-exports store, hooks, api/, slices/
    slices/
        counter-slice.ts
        index.ts
    api/
        items-api.ts  – fakeBaseQuery, in-memory data, cache tags
        index.ts
- Creates src/app/redux-page.tsx showcasing both the counter slice and RTK Query.
- Patches src/routing/router.tsx to add /redux route.
- Patches src/app/app.tsx nav to add Redux link.
- Rewrites src/main.tsx to wrap with <Provider>.
- Runs eslint --fix on all new / modified files.
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run(cmd: str) -> None:
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(f"Command failed: {cmd}")


# ---------------------------------------------------------------------------
# File contents
# ---------------------------------------------------------------------------

STORE_TS = """\
import { configureStore } from '@reduxjs/toolkit';

import { itemsApi } from './api/items-api';
import { counterReducer } from './slices/counter-slice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    [itemsApi.reducerPath]: itemsApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(itemsApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
"""

HOOKS_TS = """\
import { useDispatch, useSelector } from 'react-redux';

import type { AppDispatch, RootState } from './store';

export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector = useSelector.withTypes<RootState>();
"""

STORE_INDEX_TS = """\
export * from './api';
export * from './hooks';
export * from './slices';
export * from './store';
"""

COUNTER_SLICE_TS = """\
import { createSlice } from '@reduxjs/toolkit';

interface CounterState {
  readonly value: number;
}

const initialState: CounterState = { value: 0 };

export const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    reset: (state) => {
      state.value = 0;
    },
  },
});

export const { increment, decrement, reset } = counterSlice.actions;
export const counterReducer = counterSlice.reducer;
"""

SLICES_INDEX_TS = """\
export * from './counter-slice';
"""

ITEMS_API_TS = """\
import { createApi, fakeBaseQuery } from '@reduxjs/toolkit/query/react';

interface Item {
  readonly id: number;
  readonly name: string;
}

let nextId = 1;

const itemsDatabase: Item[] = [
  { id: nextId++, name: 'Item A' },
  { id: nextId++, name: 'Item B' },
];

export const itemsApi = createApi({
  reducerPath: 'itemsApi',
  baseQuery: fakeBaseQuery(),
  tagTypes: ['Items'],
  endpoints: (builder) => ({
    getItems: builder.query<readonly Item[], void>({
      queryFn: () => ({ data: [...itemsDatabase] }),
      providesTags: ['Items'],
    }),
    addItem: builder.mutation<Item, string>({
      queryFn: (name) => {
        const newItem: Item = { id: nextId++, name };
        itemsDatabase.push(newItem);
        return { data: newItem };
      },
      invalidatesTags: ['Items'],
    }),
  }),
});

export const { useGetItemsQuery, useAddItemMutation } = itemsApi;
"""

API_INDEX_TS = """\
export * from './items-api';
"""

REDUX_PAGE_TSX = """\
import type { CSSProperties, FormEvent } from 'react';
import { useState } from 'react';

import {
  decrement,
  increment,
  reset,
  useAddItemMutation,
  useAppDispatch,
  useAppSelector,
  useGetItemsQuery,
} from '../store';

const sectionStyle: CSSProperties = {
  marginBottom: '2rem',
};

const headingStyle: CSSProperties = {
  fontSize: '1.25rem',
  fontWeight: 600,
  marginBottom: '0.75rem',
};

const counterValueStyle: CSSProperties = {
  fontSize: '2.5rem',
  fontWeight: 700,
  marginBottom: '0.75rem',
};

const buttonGroupStyle: CSSProperties = {
  display: 'flex',
  gap: '0.5rem',
};

const buttonStyle: CSSProperties = {
  padding: '0.375rem 0.875rem',
  borderRadius: '4px',
  border: '1px solid #d1d5db',
  background: '#fff',
  cursor: 'pointer',
};

const formStyle: CSSProperties = {
  display: 'flex',
  gap: '0.5rem',
  marginBottom: '1rem',
};

const inputStyle: CSSProperties = {
  flex: 1,
  padding: '0.375rem 0.75rem',
  border: '1px solid #d1d5db',
  borderRadius: '4px',
};

const listStyle: CSSProperties = {
  listStyle: 'disc',
  paddingLeft: '1.5rem',
};

export function ReduxPage() {
  const dispatch = useAppDispatch();
  const count = useAppSelector((state) => state.counter.value);

  const { data: items = [] } = useGetItemsQuery();
  const [addItem] = useAddItemMutation();

  const [newItemName, setNewItemName] = useState('');

  function handleSubmit(e: FormEvent<HTMLFormElement>): void {
    e.preventDefault();
    const trimmed = newItemName.trim();
    if (trimmed) {
      void addItem(trimmed);
      setNewItemName('');
    }
  }

  return (
    <div>
      <h1>Redux</h1>

      <section style={sectionStyle}>
        <h2 style={headingStyle}>Counter Slice</h2>
        <div style={counterValueStyle}>{count}</div>
        <div style={buttonGroupStyle}>
          <button
            style={buttonStyle}
            onClick={() => {
              dispatch(increment());
            }}
          >
            +
          </button>
          <button
            style={buttonStyle}
            onClick={() => {
              dispatch(decrement());
            }}
          >
            −
          </button>
          <button
            style={buttonStyle}
            onClick={() => {
              dispatch(reset());
            }}
          >
            Reset
          </button>
        </div>
      </section>

      <section style={sectionStyle}>
        <h2 style={headingStyle}>RTK Query – Items</h2>
        <form style={formStyle} onSubmit={handleSubmit}>
          <input
            style={inputStyle}
            value={newItemName}
            onChange={(e) => {
              setNewItemName(e.target.value);
            }}
            placeholder='New item name'
          />
          <button style={buttonStyle} type='submit'>
            Add
          </button>
        </form>
        <ul style={listStyle}>
          {items.map((item) => (
            <li key={item.id}>{item.name}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}
"""

MAIN_TSX = """\
import './index.css';

import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';
import { RouterProvider } from 'react-router';

import { router } from './routing/router';
import { store } from './store';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  </StrictMode>,
);
"""


# ---------------------------------------------------------------------------
# Patch helpers
# ---------------------------------------------------------------------------


def patch_router_tsx() -> None:
    path = ROOT / "src" / "routing" / "router.tsx"
    src = path.read_text()

    # Add ReduxPage import (after TailwindPage import)
    src = src.replace(
        "import { TailwindPage } from '../app/tailwind-page';",
        "import { ReduxPage } from '../app/redux-page';\n"
        "import { TailwindPage } from '../app/tailwind-page';",
    )

    # Add /redux route (after tailwind child route)
    src = src.replace(
        "      { path: 'tailwind', element: <TailwindPage /> },\n    ],",
        "      { path: 'tailwind', element: <TailwindPage /> },\n"
        "      { path: 'redux', element: <ReduxPage /> },\n    ],",
    )

    path.write_text(src)
    print("  patched  src/routing/router.tsx")


def patch_app_tsx() -> None:
    path = ROOT / "src" / "app" / "app.tsx"
    src = path.read_text()

    src = src.replace(
        "        <Link style={linkStyle} to='/tailwind'>\n"
        "          Tailwind\n"
        "        </Link>\n"
        "      </nav>",
        "        <Link style={linkStyle} to='/tailwind'>\n"
        "          Tailwind\n"
        "        </Link>\n"
        "        <Link style={linkStyle} to='/redux'>\n"
        "          Redux\n"
        "        </Link>\n"
        "      </nav>",
    )

    path.write_text(src)
    print("  patched  src/app/app.tsx")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print(f"Root: {ROOT}\n")

    # [1] Install packages
    print("[1] Install @reduxjs/toolkit + react-redux")
    run("bun add @reduxjs/toolkit react-redux")
    print()

    # [2] Create store directory structure
    print("[2] Create src/store/ structure")

    store_dir = ROOT / "src" / "store"
    slices_dir = store_dir / "slices"
    api_dir = store_dir / "api"

    for d in (store_dir, slices_dir, api_dir):
        d.mkdir(parents=True, exist_ok=True)

    files = {
        store_dir / "store.ts": STORE_TS,
        store_dir / "hooks.ts": HOOKS_TS,
        store_dir / "index.ts": STORE_INDEX_TS,
        slices_dir / "counter-slice.ts": COUNTER_SLICE_TS,
        slices_dir / "index.ts": SLICES_INDEX_TS,
        api_dir / "items-api.ts": ITEMS_API_TS,
        api_dir / "index.ts": API_INDEX_TS,
    }

    for fpath, content in files.items():
        fpath.write_text(content)
        rel = fpath.relative_to(ROOT)
        print(f"  created  {rel}")

    print()

    # [3] Create redux-page.tsx
    print("[3] Create src/app/redux-page.tsx")
    redux_page = ROOT / "src" / "app" / "redux-page.tsx"
    redux_page.write_text(REDUX_PAGE_TSX)
    print("  created  src/app/redux-page.tsx\n")

    # [4] Rewrite main.tsx
    print("[4] Rewrite src/main.tsx")
    (ROOT / "src" / "main.tsx").write_text(MAIN_TSX)
    print("  written  src/main.tsx\n")

    # [5] Patch router
    print("[5] Patch src/routing/router.tsx")
    patch_router_tsx()
    print()

    # [6] Patch app.tsx nav
    print("[6] Patch src/app/app.tsx")
    patch_app_tsx()
    print()

    # [7] Fix imports / formatting
    print("[7] Fix import ordering")
    files_to_fix = " ".join(
        [
            "src/store/store.ts",
            "src/store/hooks.ts",
            "src/store/index.ts",
            "src/store/slices/counter-slice.ts",
            "src/store/slices/index.ts",
            "src/store/api/items-api.ts",
            "src/store/api/index.ts",
            "src/app/redux-page.tsx",
            "src/main.tsx",
            "src/routing/router.tsx",
            "src/app/app.tsx",
        ]
    )
    run(f"bunx eslint --fix {files_to_fix}")
    print()

    print("Done.")


if __name__ == "__main__":
    main()
