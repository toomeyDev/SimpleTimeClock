import backend, frontend
print("Boot application | main.py")

def main():
    front_end = frontend.Frontend(backend)
    front_end.mainloop()

if __name__ == '__main__':
    main()
