import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import type { Category } from '@/lib/api';
import { ChevronRight, ChevronDown, Folder, FolderOpen, Edit, Plus, Move, Trash2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { CategoryEditDialog } from './CategoryEditDialog';
import { DeleteCategoryDialog } from './DeleteCategoryDialog';

interface CategoryTreeItemProps {
  category: Category;
  selectedId: number | null;
  onSelect: (id: number) => void;
  level: number;
  taskCounts: Record<number, number>;
  noteCounts: Record<number, number>;
  editMode: boolean;
  onEdit: (category: Category, mode: 'rename' | 'move') => void;
  onAddChild: (parentCategory: Category) => void;
  onDelete: (category: Category) => void;
}

function CategoryTreeItem({ category, selectedId, onSelect, level, taskCounts, noteCounts, editMode, onEdit, onAddChild, onDelete }: CategoryTreeItemProps) {
  const [isExpanded, setIsExpanded] = useState(level === 0); // Top-level collapsed by default
  const hasChildren = category.children && category.children.length > 0;
  const isSelected = selectedId === category.id;

  const categoryButton = (
    <button
      onClick={() => !editMode && onSelect(category.id)}
      className={cn(
        "w-full flex items-center gap-2 px-3 py-2 pr-20 text-sm rounded-md transition-colors",
        isSelected && !editMode
          ? "bg-accent text-accent-foreground"
          : "hover:bg-accent/50",
        editMode && "cursor-context-menu"
      )}
    >
      <div className={cn("flex items-center gap-2 flex-1 min-w-0", level > 0 && "ml-4")}>
        {hasChildren ? (
          <button
            onClick={(e) => {
              e.stopPropagation();
              setIsExpanded(!isExpanded);
            }}
            className="flex-shrink-0 p-0.5 hover:bg-accent/70 rounded"
          >
            {isExpanded ? (
              <ChevronDown className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
          </button>
        ) : (
          <div className="w-5" />
        )}

        {isExpanded ? (
          <FolderOpen className="h-4 w-4 flex-shrink-0" />
        ) : (
          <Folder className="h-4 w-4 flex-shrink-0" />
        )}

        <span className="flex-1 text-left truncate">
          {category.name}
        </span>
      </div>
    </button>
  );

  return (
    <div>
      <div className="relative">
        {editMode ? (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              {categoryButton}
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start" className="w-48">
              <DropdownMenuItem onClick={() => onEdit(category, 'rename')}>
                <Edit className="h-4 w-4 mr-2" />
                Rename
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onAddChild(category)}>
                <Plus className="h-4 w-4 mr-2" />
                Add Subcategory
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onEdit(category, 'move')}>
                <Move className="h-4 w-4 mr-2" />
                Move to...
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => onDelete(category)} className="text-destructive">
                <Trash2 className="h-4 w-4 mr-2" />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        ) : (
          categoryButton
        )}

        {/* Badges - absolutely positioned on the right */}
        <div className="absolute right-3 top-1/2 -translate-y-1/2 flex gap-2 pointer-events-none z-10">
          {taskCounts[category.id] > 0 && (
            <span className="inline-flex items-center justify-center min-w-[24px] h-5 px-1.5 text-xs font-medium bg-blue-500 dark:bg-blue-600 text-white rounded-full">
              {taskCounts[category.id]}
            </span>
          )}
          {noteCounts[category.id] > 0 && (
            <span className="inline-flex items-center justify-center min-w-[24px] h-5 px-1.5 text-xs font-medium bg-green-500 dark:bg-green-600 text-white rounded-full">
              {noteCounts[category.id]}
            </span>
          )}
        </div>
      </div>

      {hasChildren && isExpanded && (
        <div className="mt-1">
          {category.children!.map((child) => (
            <CategoryTreeItem
              key={child.id}
              category={child}
              selectedId={selectedId}
              onSelect={onSelect}
              level={level + 1}
              taskCounts={taskCounts}
              noteCounts={noteCounts}
              editMode={editMode}
              onEdit={onEdit}
              onAddChild={onAddChild}
              onDelete={onDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}

interface CategorySidebarProps {
  onCategorySelect?: (categoryId: number | null) => void;
}

export function CategorySidebar({ onCategorySelect }: CategorySidebarProps) {
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | null>(null);
  const [editMode, setEditMode] = useState(false);

  // Edit dialog state
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editDialogMode, setEditDialogMode] = useState<'rename' | 'create' | 'move'>('rename');
  const [editingCategory, setEditingCategory] = useState<Category | undefined>(undefined);
  const [newCategoryParentId, setNewCategoryParentId] = useState<number | null>(null);

  // Delete dialog state
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingCategory, setDeletingCategory] = useState<Category | null>(null);

  const { data: categories = [], isLoading, error } = useQuery({
    queryKey: ['categories', 'tree'],
    queryFn: () => api.getCategoriesTree(),
  });

  const { data: taskCounts = {} } = useQuery({
    queryKey: ['categories', 'task-counts'],
    queryFn: () => api.getCategoryTaskCounts(),
  });

  const { data: noteCounts = {} } = useQuery({
    queryKey: ['categories', 'note-counts'],
    queryFn: () => api.getCategoryNoteCounts(),
  });

  // Calculate totals
  const totalActiveTasks = Object.values(taskCounts).reduce((sum, count) => sum + count, 0);
  const totalNotes = Object.values(noteCounts).reduce((sum, count) => sum + count, 0);

  const handleSelect = (categoryId: number) => {
    setSelectedCategoryId(categoryId);
    onCategorySelect?.(categoryId);
  };

  const handleShowAll = () => {
    setSelectedCategoryId(null);
    onCategorySelect?.(null);
  };

  const handleEdit = (category: Category, mode: 'rename' | 'move') => {
    setEditingCategory(category);
    setEditDialogMode(mode);
    setEditDialogOpen(true);
  };

  const handleAddChild = (parentCategory: Category) => {
    setNewCategoryParentId(parentCategory.id);
    setEditDialogMode('create');
    setEditDialogOpen(true);
  };

  const handleDelete = (category: Category) => {
    setDeletingCategory(category);
    setDeleteDialogOpen(true);
  };

  if (isLoading) {
    return (
      <div className="p-4 text-sm text-muted-foreground">
        Loading categories...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 text-sm text-destructive">
        Error loading categories
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="font-semibold text-lg">Categories</h2>
          <div className="flex gap-1.5">
            {totalActiveTasks > 0 && (
              <span className="px-2.5 py-1 text-xs font-semibold bg-blue-500 dark:bg-blue-600 text-white rounded-full">
                {totalActiveTasks}
              </span>
            )}
            {totalNotes > 0 && (
              <span className="px-2.5 py-1 text-xs font-semibold bg-green-500 dark:bg-green-600 text-white rounded-full">
                {totalNotes}
              </span>
            )}
          </div>
        </div>
        <Button
          variant={editMode ? "default" : "outline"}
          size="sm"
          onClick={() => setEditMode(!editMode)}
          className="w-full"
        >
          <Edit className="h-4 w-4 mr-2" />
          {editMode ? 'Exit Edit Mode' : 'Edit Categories'}
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-1">
        {/* All Tasks Option */}
        <div className="relative">
          <button
            onClick={handleShowAll}
            className={cn(
              "w-full flex items-center gap-2 px-3 py-2 pr-20 text-sm rounded-md transition-colors",
              selectedCategoryId === null
                ? "bg-accent text-accent-foreground"
                : "hover:bg-accent/50"
            )}
          >
            <div className="w-5" />
            <Folder className="h-4 w-4" />
            <span>All</span>
          </button>
          <div className="absolute right-3 top-1/2 -translate-y-1/2 flex gap-2 pointer-events-none z-10">
            {totalActiveTasks > 0 && (
              <span className="inline-flex items-center justify-center min-w-[24px] h-5 px-1.5 text-xs font-medium bg-blue-500 dark:bg-blue-600 text-white rounded-full">
                {totalActiveTasks}
              </span>
            )}
            {totalNotes > 0 && (
              <span className="inline-flex items-center justify-center min-w-[24px] h-5 px-1.5 text-xs font-medium bg-green-500 dark:bg-green-600 text-white rounded-full">
                {totalNotes}
              </span>
            )}
          </div>
        </div>

        {/* Category Tree */}
        {categories.map((category) => (
          <CategoryTreeItem
            key={category.id}
            category={category}
            selectedId={selectedCategoryId}
            onSelect={handleSelect}
            level={0}
            taskCounts={taskCounts}
            noteCounts={noteCounts}
            editMode={editMode}
            onEdit={handleEdit}
            onAddChild={handleAddChild}
            onDelete={handleDelete}
          />
        ))}
      </div>

      {/* Edit Dialog */}
      <CategoryEditDialog
        mode={editDialogMode}
        category={editingCategory}
        parentId={newCategoryParentId}
        open={editDialogOpen}
        onOpenChange={setEditDialogOpen}
      />

      {/* Delete Dialog */}
      <DeleteCategoryDialog
        category={deletingCategory}
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
      />
    </div>
  );
}
