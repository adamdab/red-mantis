from red_mantis.config.settings import Settings as settings

def main():
    print("Hello from red-mantis!")
    try:
        result = settings.FIELD_MATCH("wambo")
        print(f"FIELD_MATCH('some value') → {result}")
    except Exception as e:
        print(f"Calling FIELD_MATCH failed: {e}")


if __name__ == "__main__":
    main()
