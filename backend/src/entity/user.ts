import { Entity, PrimaryGeneratedColumn, Column } from "typeorm";

@Entity()
export class users {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column({ unique: true })
  username!: string;

  @Column()
  password!: string;

  @Column({ default: null })
  token!: string;

  @Column()
  email!: string;
}
