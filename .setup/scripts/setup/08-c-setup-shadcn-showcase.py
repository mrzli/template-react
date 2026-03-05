#!/usr/bin/env python3

# What this script does:
# - Creates src/app/examples/controls-page.tsx — showcases all shadcn controls alphabetically
# - Patches src/routing/router.tsx to add the /examples/controls route
# - Patches src/app/examples/examples-layout.tsx nav to add a Controls link
# - Runs eslint --fix on all new and modified files

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run(cmd: str) -> None:
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)


def patch_router_tsx() -> None:
    path = ROOT / "src" / "routing" / "router.tsx"
    src = path.read_text()
    if "ControlsPage" not in src:
        src = src.replace(
            "import { ReduxPage } from '../app/examples/redux-page';",
            "import { ControlsPage } from '../app/examples/controls-page';\nimport { ReduxPage } from '../app/examples/redux-page';",
        )
        src = src.replace(
            "          { path: 'redux', element: <ReduxPage /> },\n        ],",
            "          { path: 'redux', element: <ReduxPage /> },\n          { path: 'controls', element: <ControlsPage /> },\n        ],",
        )
        path.write_text(src)


def patch_examples_layout_tsx() -> None:
    path = ROOT / "src" / "app" / "examples" / "examples-layout.tsx"
    src = path.read_text()
    if "to='/examples/controls'" not in src:
        src = src.replace(
            "        <Link style={linkStyle} to='/examples/redux'>\n          Redux\n        </Link>\n      </nav>",
            "        <Link style={linkStyle} to='/examples/redux'>\n          Redux\n        </Link>\n        <Link style={linkStyle} to='/examples/controls'>\n          Controls\n        </Link>\n      </nav>",
        )
        path.write_text(src)


CONTROLS_PAGE_TSX = """\
import type { CSSProperties } from 'react';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from 'recharts';
import { toast } from 'sonner';
import { Bell, Home, Settings, User } from 'lucide-react';

import {
  type ChartConfig,
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
  Alert,
  AlertDescription,
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
  AlertTitle,
  AspectRatio,
  Avatar,
  AvatarFallback,
  AvatarImage,
  Badge,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
  Button,
  ButtonGroup,
  ButtonGroupSeparator,
  ButtonGroupText,
  Calendar,
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  Checkbox,
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
  Combobox,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger,
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
  Empty,
  EmptyContent,
  EmptyDescription,
  EmptyHeader,
  EmptyTitle,
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
  Input,
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
  InputGroupText,
  InputOTP,
  InputOTPGroup,
  InputOTPSeparator,
  InputOTPSlot,
  Item,
  ItemContent,
  ItemDescription,
  ItemGroup,
  ItemTitle,
  Kbd,
  KbdGroup,
  Label,
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarSeparator,
  MenubarTrigger,
  NativeSelect,
  NativeSelectOption,
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
  Popover,
  PopoverContent,
  PopoverTrigger,
  Progress,
  RadioGroup,
  RadioGroupItem,
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
  ScrollArea,
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
  Separator,
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarInset,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  Skeleton,
  Slider,
  Spinner,
  Switch,
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
  Textarea,
  Toggle,
  ToggleGroup,
  ToggleGroupItem,
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
  Toaster,
} from '@/controls';

// ─── chart data ────────────────────────────────────────────────────────────────

const chartData = [
  { month: 'Jan', value: 186 },
  { month: 'Feb', value: 305 },
  { month: 'Mar', value: 237 },
  { month: 'Apr', value: 73 },
  { month: 'May', value: 209 },
  { month: 'Jun', value: 214 },
];

const chartConfig: ChartConfig = {
  value: { label: 'Value', color: 'hsl(var(--chart-1))' },
};

// ─── layout helpers ────────────────────────────────────────────────────────────

const pageStyle: CSSProperties = {
  paddingBottom: '4rem',
};

const headingStyle: CSSProperties = {
  fontSize: '1.5rem',
  fontWeight: 700,
  marginBottom: '2rem',
};

const sectionStyle: CSSProperties = {
  marginBottom: '1.5rem',
  padding: '1rem',
  border: '1px solid #e5e7eb',
  borderRadius: '8px',
  background: '#fff',
};

const sectionTitleStyle: CSSProperties = {
  fontSize: '0.875rem',
  fontWeight: 600,
  marginBottom: '0.75rem',
  color: '#6b7280',
  textTransform: 'uppercase',
  letterSpacing: '0.05em',
};

const rowStyle: CSSProperties = {
  display: 'flex',
  flexWrap: 'wrap',
  gap: '0.5rem',
  alignItems: 'flex-start',
};

interface SectionProps {
  readonly title: string;
  readonly children: React.ReactNode;
  readonly block?: boolean;
}

function Section({ title, children, block = false }: SectionProps) {
  return (
    <div style={sectionStyle}>
      <div style={sectionTitleStyle}>{title}</div>
      <div style={block ? { display: 'flex', flexDirection: 'column', gap: '0.75rem' } : rowStyle}>
        {children}
      </div>
    </div>
  );
}

// ─── showcase form helper ──────────────────────────────────────────────────────

interface ShowcaseFormValues {
  username: string;
}

function ShowcaseForm() {
  const form = useForm<ShowcaseFormValues>({
    defaultValues: { username: '' },
  });

  function onSubmit(values: ShowcaseFormValues): void {
    console.log(values);
  }

  return (
    <Form {...form}>
      <form className='w-72 space-y-4' onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name='username'
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                <Input placeholder='your-username' {...field} />
              </FormControl>
              <FormDescription>Your public display name.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button size='sm' type='submit'>
          Submit
        </Button>
      </form>
    </Form>
  );
}

// ─── page ──────────────────────────────────────────────────────────────────────

export function ControlsPage() {
  const [checkboxChecked, setCheckboxChecked] = useState(false);
  const [switchChecked, setSwitchChecked] = useState(false);
  const [sliderValue, setSliderValue] = useState([50]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [alertDialogOpen, setAlertDialogOpen] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [sheetOpen, setSheetOpen] = useState(false);
  const [calendarDate, setCalendarDate] = useState<Date | undefined>(new Date());
  const [radioValue, setRadioValue] = useState('opt1');
  const [togglePressed, setTogglePressed] = useState(false);
  const [toggleGroupValue, setToggleGroupValue] = useState('left');
  const [collapsibleOpen, setCollapsibleOpen] = useState(false);
  const [inputOtpValue, setInputOtpValue] = useState('');
  const [progressValue] = useState(62);

  return (
    <TooltipProvider>
      <div style={pageStyle}>
        <Toaster />
        <h1 style={headingStyle}>Controls Showcase</h1>

        {/* ── Accordion ─────────────────────────────────────── */}
        <Section title='Accordion' block>
          <Accordion className='w-80' collapsible type='single'>
            <AccordionItem value='item-1'>
              <AccordionTrigger>What is shadcn/ui?</AccordionTrigger>
              <AccordionContent>
                A set of accessible, composable React components built with Radix
                UI and Tailwind CSS.
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value='item-2'>
              <AccordionTrigger>Is it free?</AccordionTrigger>
              <AccordionContent>Yes. Open source and free to use.</AccordionContent>
            </AccordionItem>
          </Accordion>
        </Section>

        {/* ── Alert ─────────────────────────────────────────── */}
        <Section title='Alert' block>
          <Alert className='w-96'>
            <Bell className='size-4' />
            <AlertTitle>Default alert</AlertTitle>
            <AlertDescription>Something happened that you should know about.</AlertDescription>
          </Alert>
          <Alert className='w-96' variant='destructive'>
            <Bell className='size-4' />
            <AlertTitle>Destructive alert</AlertTitle>
            <AlertDescription>This action cannot be undone.</AlertDescription>
          </Alert>
        </Section>

        {/* ── AlertDialog ───────────────────────────────────── */}
        <Section title='AlertDialog'>
          <AlertDialog open={alertDialogOpen} onOpenChange={setAlertDialogOpen}>
            <AlertDialogTrigger asChild>
              <Button variant='outline'>Open Alert Dialog</Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                <AlertDialogDescription>
                  This action cannot be undone. This will permanently delete your
                  account.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction>Continue</AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </Section>

        {/* ── AspectRatio ───────────────────────────────────── */}
        <Section title='AspectRatio'>
          <div className='w-64'>
            <AspectRatio ratio={16 / 9}>
              <div className='flex size-full items-center justify-center rounded-lg bg-muted text-sm text-muted-foreground'>
                16 / 9
              </div>
            </AspectRatio>
          </div>
        </Section>

        {/* ── Avatar ────────────────────────────────────────── */}
        <Section title='Avatar'>
          <Avatar>
            <AvatarImage alt='User' src='https://github.com/shadcn.png' />
            <AvatarFallback>SC</AvatarFallback>
          </Avatar>
          <Avatar>
            <AvatarFallback>JD</AvatarFallback>
          </Avatar>
        </Section>

        {/* ── Badge ─────────────────────────────────────────── */}
        <Section title='Badge'>
          <Badge>Default</Badge>
          <Badge variant='secondary'>Secondary</Badge>
          <Badge variant='destructive'>Destructive</Badge>
          <Badge variant='outline'>Outline</Badge>
        </Section>

        {/* ── Breadcrumb ────────────────────────────────────── */}
        <Section title='Breadcrumb'>
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink href='/'>Home</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbLink href='/controls'>Controls</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbPage>Showcase</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </Section>

        {/* ── Button ────────────────────────────────────────── */}
        <Section title='Button'>
          <Button>Default</Button>
          <Button variant='secondary'>Secondary</Button>
          <Button variant='destructive'>Destructive</Button>
          <Button variant='outline'>Outline</Button>
          <Button variant='ghost'>Ghost</Button>
          <Button variant='link'>Link</Button>
          <Button size='sm'>Small</Button>
          <Button size='lg'>Large</Button>
          <Button disabled>Disabled</Button>
        </Section>

        {/* ── ButtonGroup ───────────────────────────────────── */}
        <Section title='ButtonGroup'>
          <ButtonGroup>
            <Button variant='outline'>Left</Button>
            <Button variant='outline'>Center</Button>
            <Button variant='outline'>Right</Button>
          </ButtonGroup>
          <ButtonGroup>
            <Button variant='outline'>Action</Button>
            <ButtonGroupSeparator />
            <Button variant='outline'><Bell className='size-4' /></Button>
          </ButtonGroup>
          <ButtonGroup>
            <ButtonGroupText>Prefix</ButtonGroupText>
            <Button>Submit</Button>
          </ButtonGroup>
        </Section>

        {/* ── Calendar ──────────────────────────────────────── */}
        <Section title='Calendar'>
          <Calendar
            mode='single'
            selected={calendarDate}
            onSelect={setCalendarDate}
          />
        </Section>

        {/* ── Card ──────────────────────────────────────────── */}
        <Section title='Card'>
          <Card className='w-72'>
            <CardHeader>
              <CardTitle>Card Title</CardTitle>
              <CardDescription>Card description goes here.</CardDescription>
            </CardHeader>
            <CardContent>
              <p className='text-sm'>Card body content.</p>
            </CardContent>
            <CardFooter className='gap-2'>
              <Button size='sm'>Save</Button>
              <Button size='sm' variant='outline'>Cancel</Button>
            </CardFooter>
          </Card>
        </Section>

        {/* ── Carousel ──────────────────────────────────────── */}
        <Section title='Carousel'>
          <Carousel className='w-72'>
            <CarouselContent>
              {[1, 2, 3, 4].map((n) => (
                <CarouselItem key={n}>
                  <div className='flex aspect-square items-center justify-center rounded-lg bg-muted text-2xl font-bold'>
                    {n}
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </Section>

        {/* ── Chart ─────────────────────────────────────────── */}
        <Section title='Chart'>
          <ChartContainer className='h-48 w-96' config={chartConfig}>
            <BarChart data={chartData}>
              <CartesianGrid vertical={false} />
              <XAxis dataKey='month' tickLine={false} />
              <YAxis axisLine={false} tickLine={false} />
              <ChartTooltip content={<ChartTooltipContent />} />
              <Bar dataKey='value' fill='var(--color-value)' radius={4} />
            </BarChart>
          </ChartContainer>
        </Section>

        {/* ── Checkbox ──────────────────────────────────────── */}
        <Section title='Checkbox'>
          <div className='flex items-center gap-2'>
            <Checkbox
              id='cb1'
              checked={checkboxChecked}
              onCheckedChange={(v) => {
                setCheckboxChecked(v === true);
              }}
            />
            <Label htmlFor='cb1'>Accept terms and conditions</Label>
          </div>
          <div className='flex items-center gap-2'>
            <Checkbox id='cb2' defaultChecked />
            <Label htmlFor='cb2'>Default checked</Label>
          </div>
          <div className='flex items-center gap-2'>
            <Checkbox id='cb3' disabled />
            <Label htmlFor='cb3'>Disabled</Label>
          </div>
        </Section>

        {/* ── Collapsible ───────────────────────────────────── */}
        <Section title='Collapsible' block>
          <Collapsible
            className='w-64'
            open={collapsibleOpen}
            onOpenChange={setCollapsibleOpen}
          >
            <CollapsibleTrigger asChild>
              <Button className='w-full justify-between' variant='outline'>
                Show details
              </Button>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <div className='mt-2 rounded-lg border bg-muted/50 p-3 text-sm'>
                Hidden content revealed on expand.
              </div>
            </CollapsibleContent>
          </Collapsible>
        </Section>

        {/* ── Combobox ──────────────────────────────────────── */}
        <Section title='Combobox'>
          <Combobox>
            <ComboboxInput className='w-48' placeholder='Select fruit...' />
            <ComboboxContent>
              <ComboboxList>
                <ComboboxEmpty>No results found.</ComboboxEmpty>
                <ComboboxItem value='apple'>Apple</ComboboxItem>
                <ComboboxItem value='banana'>Banana</ComboboxItem>
                <ComboboxItem value='cherry'>Cherry</ComboboxItem>
                <ComboboxItem value='mango'>Mango</ComboboxItem>
              </ComboboxList>
            </ComboboxContent>
          </Combobox>
        </Section>

        {/* ── Command ───────────────────────────────────────── */}
        <Section title='Command'>
          <Command className='w-72 rounded-lg border shadow-md'>
            <CommandInput placeholder='Type a command...' />
            <CommandList>
              <CommandEmpty>No results found.</CommandEmpty>
              <CommandGroup heading='Actions'>
                <CommandItem>
                  <Home className='size-4' />
                  Go Home
                </CommandItem>
                <CommandItem>
                  <Settings className='size-4' />
                  Settings
                </CommandItem>
                <CommandItem>
                  <User className='size-4' />
                  Profile
                </CommandItem>
              </CommandGroup>
            </CommandList>
          </Command>
        </Section>

        {/* ── ContextMenu ───────────────────────────────────── */}
        <Section title='ContextMenu'>
          <ContextMenu>
            <ContextMenuTrigger asChild>
              <div className='flex h-20 w-48 items-center justify-center rounded-lg border border-dashed text-sm text-muted-foreground'>
                Right-click here
              </div>
            </ContextMenuTrigger>
            <ContextMenuContent>
              <ContextMenuItem>Copy</ContextMenuItem>
              <ContextMenuItem>Paste</ContextMenuItem>
              <ContextMenuItem>Delete</ContextMenuItem>
            </ContextMenuContent>
          </ContextMenu>
        </Section>

        {/* ── Dialog ────────────────────────────────────────── */}
        <Section title='Dialog'>
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button variant='outline'>Open Dialog</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Edit Profile</DialogTitle>
                <DialogDescription>
                  Make changes to your profile here. Click save when done.
                </DialogDescription>
              </DialogHeader>
              <div className='py-2'>
                <Input placeholder='Display name' />
              </div>
              <DialogFooter>
                <DialogClose asChild>
                  <Button variant='outline'>Cancel</Button>
                </DialogClose>
                <Button>Save changes</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </Section>

        {/* ── Drawer ────────────────────────────────────────── */}
        <Section title='Drawer'>
          <Drawer open={drawerOpen} onOpenChange={setDrawerOpen}>
            <DrawerTrigger asChild>
              <Button variant='outline'>Open Drawer</Button>
            </DrawerTrigger>
            <DrawerContent>
              <DrawerHeader>
                <DrawerTitle>Drawer Title</DrawerTitle>
                <DrawerDescription>Drawer description text.</DrawerDescription>
              </DrawerHeader>
              <div className='p-4'>
                <p className='text-sm'>Drawer body content goes here.</p>
              </div>
              <DrawerFooter>
                <DrawerClose asChild>
                  <Button variant='outline'>Close</Button>
                </DrawerClose>
              </DrawerFooter>
            </DrawerContent>
          </Drawer>
        </Section>

        {/* ── DropdownMenu ──────────────────────────────────── */}
        <Section title='DropdownMenu'>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant='outline'>Open Dropdown</Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuLabel>My Account</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Profile</DropdownMenuItem>
              <DropdownMenuItem>Billing</DropdownMenuItem>
              <DropdownMenuItem>Settings</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Log out</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </Section>

        {/* ── Empty ─────────────────────────────────────────── */}
        <Section title='Empty'>
          <Empty className='w-64 rounded-lg border p-6'>
            <EmptyHeader>
              <EmptyTitle>No results</EmptyTitle>
            </EmptyHeader>
            <EmptyContent>
              <EmptyDescription>
                Try adjusting your filters to find what you're looking for.
              </EmptyDescription>
            </EmptyContent>
          </Empty>
        </Section>

        {/* ── Field ─────────────────────────────────────────── */}
        <Section title='Field' block>
          <FieldGroup className='w-80'>
            <Field>
              <FieldLabel>Full name</FieldLabel>
              <Input placeholder='John Doe' />
              <FieldDescription>Your legal full name.</FieldDescription>
            </Field>
            <Field data-invalid='true'>
              <FieldLabel>Email</FieldLabel>
              <Input placeholder='john@example.com' type='email' />
              <FieldError>Please enter a valid email address.</FieldError>
            </Field>
          </FieldGroup>
        </Section>

        {/* ── Form ──────────────────────────────────────────── */}
        <Section title='Form'>
          <ShowcaseForm />
        </Section>

        {/* ── HoverCard ─────────────────────────────────────── */}
        <Section title='HoverCard'>
          <HoverCard>
            <HoverCardTrigger asChild>
              <Button variant='link'>@shadcn</Button>
            </HoverCardTrigger>
            <HoverCardContent className='w-64'>
              <div className='flex items-center gap-3'>
                <Avatar>
                  <AvatarImage src='https://github.com/shadcn.png' />
                  <AvatarFallback>SC</AvatarFallback>
                </Avatar>
                <div>
                  <p className='text-sm font-semibold'>@shadcn</p>
                  <p className='text-xs text-muted-foreground'>
                    Building UI components.
                  </p>
                </div>
              </div>
            </HoverCardContent>
          </HoverCard>
        </Section>

        {/* ── Input ─────────────────────────────────────────── */}
        <Section title='Input' block>
          <Input className='w-64' placeholder='Default input' />
          <Input className='w-64' disabled placeholder='Disabled input' />
          <Input className='w-64' placeholder='Password' type='password' />
        </Section>

        {/* ── InputGroup ────────────────────────────────────── */}
        <Section title='InputGroup' block>
          <InputGroup className='w-64'>
            <InputGroupAddon align='inline-start'>
              <InputGroupText>https://</InputGroupText>
            </InputGroupAddon>
            <InputGroupInput placeholder='yoursite.com' />
          </InputGroup>
        </Section>

        {/* ── InputOTP ──────────────────────────────────────── */}
        <Section title='InputOTP'>
          <InputOTP maxLength={6} value={inputOtpValue} onChange={setInputOtpValue}>
            <InputOTPGroup>
              <InputOTPSlot index={0} />
              <InputOTPSlot index={1} />
              <InputOTPSlot index={2} />
            </InputOTPGroup>
            <InputOTPSeparator />
            <InputOTPGroup>
              <InputOTPSlot index={3} />
              <InputOTPSlot index={4} />
              <InputOTPSlot index={5} />
            </InputOTPGroup>
          </InputOTP>
        </Section>

        {/* ── Item ──────────────────────────────────────────── */}
        <Section title='Item' block>
          <ItemGroup className='w-80 rounded-lg border'>
            <Item>
              <ItemContent>
                <ItemTitle>First item</ItemTitle>
                <ItemDescription>Description of the first item.</ItemDescription>
              </ItemContent>
            </Item>
            <Item>
              <ItemContent>
                <ItemTitle>Second item</ItemTitle>
                <ItemDescription>Description of the second item.</ItemDescription>
              </ItemContent>
            </Item>
          </ItemGroup>
        </Section>

        {/* ── Kbd ───────────────────────────────────────────── */}
        <Section title='Kbd'>
          <KbdGroup>
            <Kbd>⌘</Kbd>
            <Kbd>K</Kbd>
          </KbdGroup>
          <KbdGroup>
            <Kbd>Ctrl</Kbd>
            <Kbd>Shift</Kbd>
            <Kbd>P</Kbd>
          </KbdGroup>
        </Section>

        {/* ── Label ─────────────────────────────────────────── */}
        <Section title='Label'>
          <div className='flex flex-col gap-1'>
            <Label htmlFor='demo-input'>Email address</Label>
            <Input className='w-48' id='demo-input' type='email' />
          </div>
        </Section>

        {/* ── Menubar ───────────────────────────────────────── */}
        <Section title='Menubar'>
          <Menubar>
            <MenubarMenu>
              <MenubarTrigger>File</MenubarTrigger>
              <MenubarContent>
                <MenubarItem>New</MenubarItem>
                <MenubarItem>Open</MenubarItem>
                <MenubarSeparator />
                <MenubarItem>Save</MenubarItem>
              </MenubarContent>
            </MenubarMenu>
            <MenubarMenu>
              <MenubarTrigger>Edit</MenubarTrigger>
              <MenubarContent>
                <MenubarItem>Undo</MenubarItem>
                <MenubarItem>Redo</MenubarItem>
              </MenubarContent>
            </MenubarMenu>
          </Menubar>
        </Section>

        {/* ── NativeSelect ──────────────────────────────────── */}
        <Section title='NativeSelect'>
          <NativeSelect className='w-48'>
            <NativeSelectOption value=''>Pick a fruit...</NativeSelectOption>
            <NativeSelectOption value='apple'>Apple</NativeSelectOption>
            <NativeSelectOption value='banana'>Banana</NativeSelectOption>
            <NativeSelectOption value='cherry'>Cherry</NativeSelectOption>
          </NativeSelect>
        </Section>

        {/* ── NavigationMenu ────────────────────────────────── */}
        <Section title='NavigationMenu'>
          <NavigationMenu>
            <NavigationMenuList>
              <NavigationMenuItem>
                <NavigationMenuLink className='px-4 py-2 text-sm font-medium' href='/'>
                  Home
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <NavigationMenuLink className='px-4 py-2 text-sm font-medium' href='/controls'>
                  Controls
                </NavigationMenuLink>
              </NavigationMenuItem>
            </NavigationMenuList>
          </NavigationMenu>
        </Section>

        {/* ── Pagination ────────────────────────────────────── */}
        <Section title='Pagination'>
          <Pagination>
            <PaginationContent>
              <PaginationItem>
                <PaginationPrevious href='#' />
              </PaginationItem>
              <PaginationItem>
                <PaginationLink href='#'>1</PaginationLink>
              </PaginationItem>
              <PaginationItem>
                <PaginationLink href='#' isActive>2</PaginationLink>
              </PaginationItem>
              <PaginationItem>
                <PaginationLink href='#'>3</PaginationLink>
              </PaginationItem>
              <PaginationItem>
                <PaginationEllipsis />
              </PaginationItem>
              <PaginationItem>
                <PaginationNext href='#' />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        </Section>

        {/* ── Popover ───────────────────────────────────────── */}
        <Section title='Popover'>
          <Popover>
            <PopoverTrigger asChild>
              <Button variant='outline'>Open Popover</Button>
            </PopoverTrigger>
            <PopoverContent className='w-64'>
              <p className='text-sm font-medium'>Popover content</p>
              <p className='mt-1 text-sm text-muted-foreground'>
                This is the popover body text.
              </p>
            </PopoverContent>
          </Popover>
        </Section>

        {/* ── Progress ──────────────────────────────────────── */}
        <Section title='Progress' block>
          <Progress className='w-72' value={progressValue} />
          <Progress className='w-72' value={100} />
          <Progress className='w-72' value={0} />
        </Section>

        {/* ── RadioGroup ────────────────────────────────────── */}
        <Section title='RadioGroup' block>
          <RadioGroup value={radioValue} onValueChange={setRadioValue}>
            <div className='flex items-center gap-2'>
              <RadioGroupItem id='opt1' value='opt1' />
              <Label htmlFor='opt1'>Option one</Label>
            </div>
            <div className='flex items-center gap-2'>
              <RadioGroupItem id='opt2' value='opt2' />
              <Label htmlFor='opt2'>Option two</Label>
            </div>
            <div className='flex items-center gap-2'>
              <RadioGroupItem disabled id='opt3' value='opt3' />
              <Label htmlFor='opt3'>Option three (disabled)</Label>
            </div>
          </RadioGroup>
        </Section>

        {/* ── Resizable ─────────────────────────────────────── */}
        <Section title='Resizable'>
          <ResizablePanelGroup className='h-32 w-80 rounded-lg border'>
            <ResizablePanel defaultSize={50}>
              <div className='flex h-full items-center justify-center text-sm'>
                Left
              </div>
            </ResizablePanel>
            <ResizableHandle />
            <ResizablePanel defaultSize={50}>
              <div className='flex h-full items-center justify-center text-sm'>
                Right
              </div>
            </ResizablePanel>
          </ResizablePanelGroup>
        </Section>

        {/* ── ScrollArea ────────────────────────────────────── */}
        <Section title='ScrollArea'>
          <ScrollArea className='h-40 w-64 rounded-lg border p-3'>
            {Array.from({ length: 20 }, (_, i) => (
              <p key={i} className='py-0.5 text-sm'>
                Item {i + 1}
              </p>
            ))}
          </ScrollArea>
        </Section>

        {/* ── Select ────────────────────────────────────────── */}
        <Section title='Select'>
          <Select>
            <SelectTrigger className='w-48'>
              <SelectValue placeholder='Select a fruit' />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value='apple'>Apple</SelectItem>
              <SelectItem value='banana'>Banana</SelectItem>
              <SelectItem value='cherry'>Cherry</SelectItem>
            </SelectContent>
          </Select>
        </Section>

        {/* ── Separator ─────────────────────────────────────── */}
        <Section title='Separator' block>
          <div className='w-64'>
            <p className='text-sm'>Above separator</p>
            <Separator className='my-2' />
            <p className='text-sm'>Below separator</p>
          </div>
          <div className='flex h-8 items-center gap-4'>
            <span className='text-sm'>A</span>
            <Separator orientation='vertical' />
            <span className='text-sm'>B</span>
            <Separator orientation='vertical' />
            <span className='text-sm'>C</span>
          </div>
        </Section>

        {/* ── Sheet ─────────────────────────────────────────── */}
        <Section title='Sheet'>
          <Sheet open={sheetOpen} onOpenChange={setSheetOpen}>
            <SheetTrigger asChild>
              <Button variant='outline'>Open Sheet</Button>
            </SheetTrigger>
            <SheetContent>
              <SheetHeader>
                <SheetTitle>Sheet Title</SheetTitle>
                <SheetDescription>
                  Sheet slide-in panel description.
                </SheetDescription>
              </SheetHeader>
              <div className='py-4'>
                <p className='text-sm'>Sheet body content.</p>
              </div>
              <SheetFooter>
                <SheetClose asChild>
                  <Button variant='outline'>Close</Button>
                </SheetClose>
              </SheetFooter>
            </SheetContent>
          </Sheet>
        </Section>

        {/* ── Sidebar ───────────────────────────────────────── */}
        <Section title='Sidebar'>
          <div style={{ height: 200, width: 400, overflow: 'hidden', border: '1px solid #e5e7eb', borderRadius: 8 }}>
            <SidebarProvider style={{ '--sidebar-width': '180px' } as CSSProperties}>
              <div className='flex size-full'>
                <div className='flex h-full flex-col' style={{ width: 180, borderRight: '1px solid #e5e7eb' }}>
                  <SidebarContent>
                    <SidebarGroup>
                      <SidebarGroupLabel>Navigation</SidebarGroupLabel>
                      <SidebarGroupContent>
                        <SidebarMenu>
                          <SidebarMenuItem>
                            <SidebarMenuButton>
                              <Home className='size-4' />
                              Home
                            </SidebarMenuButton>
                          </SidebarMenuItem>
                          <SidebarMenuItem>
                            <SidebarMenuButton>
                              <Settings className='size-4' />
                              Settings
                            </SidebarMenuButton>
                          </SidebarMenuItem>
                          <SidebarMenuItem>
                            <SidebarMenuButton>
                              <User className='size-4' />
                              Profile
                            </SidebarMenuButton>
                          </SidebarMenuItem>
                        </SidebarMenu>
                      </SidebarGroupContent>
                    </SidebarGroup>
                  </SidebarContent>
                </div>
                <SidebarInset className='flex flex-1 items-center justify-center text-sm text-muted-foreground'>
                  Main content area
                </SidebarInset>
              </div>
            </SidebarProvider>
          </div>
        </Section>

        {/* ── Skeleton ──────────────────────────────────────── */}
        <Section title='Skeleton' block>
          <div className='flex items-center gap-4'>
            <Skeleton className='size-12 rounded-full' />
            <div className='flex flex-col gap-2'>
              <Skeleton className='h-4 w-48' />
              <Skeleton className='h-4 w-32' />
            </div>
          </div>
        </Section>

        {/* ── Slider ────────────────────────────────────────── */}
        <Section title='Slider' block>
          <Slider
            className='w-64'
            max={100}
            step={1}
            value={sliderValue}
            onValueChange={setSliderValue}
          />
          <p className='text-sm text-muted-foreground'>Value: {sliderValue[0]}</p>
        </Section>

        {/* ── Sonner (Toaster) ──────────────────────────────── */}
        <Section title='Sonner'>
          <Button
            variant='outline'
            onClick={() => {
              toast('Event has been created', {
                description: 'Monday, January 3rd at 6:00pm',
                action: { label: 'Undo', onClick: () => {} },
              });
            }}
          >
            Show Toast
          </Button>
          <Button
            variant='outline'
            onClick={() => {
              toast.success('Changes saved successfully!');
            }}
          >
            Success Toast
          </Button>
          <Button
            variant='outline'
            onClick={() => {
              toast.error('Something went wrong.');
            }}
          >
            Error Toast
          </Button>
        </Section>

        {/* ── Spinner ───────────────────────────────────────── */}
        <Section title='Spinner'>
          <Spinner className='size-4' />
          <Spinner className='size-6' />
          <Spinner className='size-8' />
        </Section>

        {/* ── Switch ────────────────────────────────────────── */}
        <Section title='Switch'>
          <div className='flex items-center gap-2'>
            <Switch
              id='sw1'
              checked={switchChecked}
              onCheckedChange={setSwitchChecked}
            />
            <Label htmlFor='sw1'>
              {switchChecked ? 'Enabled' : 'Disabled'}
            </Label>
          </div>
          <div className='flex items-center gap-2'>
            <Switch id='sw2' defaultChecked />
            <Label htmlFor='sw2'>Notifications</Label>
          </div>
        </Section>

        {/* ── Table ─────────────────────────────────────────── */}
        <Section title='Table'>
          <Table className='w-96'>
            <TableCaption>A list of recent invoices.</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Invoice</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className='text-right'>Amount</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell>INV-001</TableCell>
                <TableCell>Paid</TableCell>
                <TableCell className='text-right'>$250.00</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>INV-002</TableCell>
                <TableCell>Pending</TableCell>
                <TableCell className='text-right'>$150.00</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>INV-003</TableCell>
                <TableCell>Unpaid</TableCell>
                <TableCell className='text-right'>$350.00</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </Section>

        {/* ── Tabs ──────────────────────────────────────────── */}
        <Section title='Tabs'>
          <Tabs className='w-72' defaultValue='account'>
            <TabsList>
              <TabsTrigger value='account'>Account</TabsTrigger>
              <TabsTrigger value='password'>Password</TabsTrigger>
              <TabsTrigger disabled value='billing'>Billing</TabsTrigger>
            </TabsList>
            <TabsContent value='account'>
              <p className='p-2 text-sm'>Account settings content.</p>
            </TabsContent>
            <TabsContent value='password'>
              <p className='p-2 text-sm'>Password settings content.</p>
            </TabsContent>
          </Tabs>
        </Section>

        {/* ── Textarea ──────────────────────────────────────── */}
        <Section title='Textarea' block>
          <Textarea className='w-64' placeholder='Type your message here...' />
          <Textarea className='w-64' disabled placeholder='Disabled textarea' />
        </Section>

        {/* ── Toggle ────────────────────────────────────────── */}
        <Section title='Toggle'>
          <Toggle pressed={togglePressed} onPressedChange={setTogglePressed}>
            <Bell className='size-4' />
            Notifications {togglePressed ? 'On' : 'Off'}
          </Toggle>
          <Toggle variant='outline'>
            <Settings className='size-4' />
            Settings
          </Toggle>
          <Toggle disabled>Disabled</Toggle>
        </Section>

        {/* ── ToggleGroup ───────────────────────────────────── */}
        <Section title='ToggleGroup'>
          <ToggleGroup
            type='single'
            value={toggleGroupValue}
            onValueChange={(v) => {
              if (v) {
                setToggleGroupValue(v);
              }
            }}
          >
            <ToggleGroupItem value='left'>Left</ToggleGroupItem>
            <ToggleGroupItem value='center'>Center</ToggleGroupItem>
            <ToggleGroupItem value='right'>Right</ToggleGroupItem>
          </ToggleGroup>
        </Section>

        {/* ── Tooltip ───────────────────────────────────────── */}
        <Section title='Tooltip'>
          <Tooltip>
            <TooltipTrigger asChild>
              <Button variant='outline'>Hover me</Button>
            </TooltipTrigger>
            <TooltipContent>
              <p>This is a tooltip</p>
            </TooltipContent>
          </Tooltip>
          <Tooltip>
            <TooltipTrigger asChild>
              <Button size='icon' variant='outline'>
                <Settings className='size-4' />
              </Button>
            </TooltipTrigger>
            <TooltipContent side='right'>
              <p>Settings</p>
            </TooltipContent>
          </Tooltip>
        </Section>
      </div>
    </TooltipProvider>
  );
}
"""


def main() -> None:
    print(f"Root: {ROOT}\n")

    # 1. Create src/app/examples/controls-page.tsx
    print("[1] Create src/app/examples/controls-page.tsx")
    (ROOT / "src" / "app" / "examples" / "controls-page.tsx").write_text(
        CONTROLS_PAGE_TSX
    )
    print("  created  src/app/examples/controls-page.tsx")

    # 2. Patch src/routing/router.tsx
    print("\n[2] Patch src/routing/router.tsx")
    patch_router_tsx()
    print("  patched  src/routing/router.tsx")

    # 3. Patch src/app/examples/examples-layout.tsx nav
    print("\n[3] Patch src/app/examples/examples-layout.tsx")
    patch_examples_layout_tsx()
    print("  patched  src/app/examples/examples-layout.tsx")

    # 4. Fix import ordering
    print("\n[4] Fix import ordering")
    run(
        "bunx eslint --fix src/app/examples/controls-page.tsx src/routing/router.tsx src/app/examples/examples-layout.tsx"
    )

    print("\nDone.")


main()
