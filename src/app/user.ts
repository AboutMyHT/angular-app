export class User {
    constructor(
        public email: string,
        public zipCode: string,
        public firstName: string,
        public lastName: string,
        public emailVerified: boolean,
        public needsPasswordReset: boolean
    ) { };

    static fromObject(data: any): User {
        return new User(data.email, data.zip_code, data.first_name, data.last_name, data.email_verified, data.needs_password_reset);
    }

    public fiveDigitZip(): number {
        return Number(this.zipCode.slice(0, 5));
    }

    public displayName(): string {
        if (this.firstName) {
            return `${this.firstName} ${this.lastName}`;
        }
        return this.email;
    }

    public toString(): string {
        return `User: (Name: '${this.firstName} ${this.lastName}', Email: ${this.email}, Zip: ${this.zipCode}, Email Verified: ${this.emailVerified}, Needs Password Reset: ${this.needsPasswordReset})`;
    }
}